package main

import (
	"context"
	"errors"
	"fmt"
	"log"
	"net/http"
	"net/http/httputil"
	"sync"
)

type ResponseTime struct {
	r   float64
	url string
}

type Request struct {
	w  http.ResponseWriter
	r  *http.Request
	ch chan struct{}
}

var (
	proxys           map[string]*httputil.ReverseProxy = make(map[string]*httputil.ReverseProxy)
	balancers        map[int]chan ResponseTime         = make(map[int]chan ResponseTime)
	wg               sync.WaitGroup
	reqsCh           chan Request                             = make(chan Request)
	balancersReadyCh chan struct{}                            = make(chan struct{})
	httpHandler      func(http.ResponseWriter, *http.Request) = func(w http.ResponseWriter, r *http.Request) {
		ch := make(chan struct{})
		reqsCh <- Request{
			w:  w,
			r:  r,
			ch: ch,
		}
		<-ch
		close(ch)
	}
	tmp map[string]int = make(map[string]int)
)

func loadBalance(ctx context.Context, backendsURLS []string, port int) (err error) {
	for _, url := range backendsURLS {
		// create proxys
		proxy, err := NewProxy(url)
		if err != nil {
			return err
		}
		log.Printf("Proxy for %s ready!", url)
		proxys[url] = proxy
	}

	for i := 0; i < len(backendsURLS); i++ {
		wg.Add(1)
		balancers[i] = make(chan ResponseTime)
		go balancer(ctx, wg, backendsURLS, i)
	}
	// wait that balancers are ready
	for i := 0; i < len(backendsURLS); i++ {
		<-balancersReadyCh
	}
	log.Printf("%d balancers ready to work!", len(backendsURLS))

	server := http.Server{
		Addr:    fmt.Sprintf(":%d", port),
		Handler: http.HandlerFunc(httpHandler),
	}
	// listen for client http request
	log.Printf("HTTP server listening at localhost:%d", port)
	err = server.ListenAndServe()
	if err != nil {
		return err
	}

	// wait for probe the be ended
	wg.Wait()
	log.Printf("Balancers shutdown succesfully")
	return nil
}

func balancer(ctx context.Context, wg sync.WaitGroup, backendsURLS []string, id int) {
	var url string
	// sum of the mean of response time of every balanced server
	var sumRespTm float64
	var err error
	servers := make(map[string]float64)
	randomValue := 100.0
	for _, url := range backendsURLS {
		sumRespTm += randomValue
		servers[url] = randomValue
	}
	metricsCh := balancers[id]
	// ready to go! (or almost)
	balancersReadyCh <- struct{}{}
	for {
		select {
		case req := <-reqsCh:
			// IDEA -> make this getForwardURL every x iteration in worker so don't have to re compute everything, (only if is a limitation)
			url, err = getForwardURL(servers, sumRespTm)
			if err != nil {
				log.Print(fmt.Errorf("got err on choosing backend URL %v", err))
				go func() {
					reqsCh <- req
				}()
			}
			tmp[url]++
			go balance(url, req)
		case metric := <-metricsCh:
			sumRespTm -= servers[metric.url]
			scaledValue := scaledMean(metric.r, servers[metric.url], 50.0)
			servers[metric.url] = scaledValue + servers[metric.url]
			sumRespTm += servers[metric.url]
		case <-ctx.Done():
			wg.Done()
			return
		}
	}
}

func balance(URL string, req Request) {
	proxys[URL].ServeHTTP(req.w, req.r)
	req.ch <- struct{}{}
}

// return the forwardURL
func getForwardURL(servers map[string]float64, sumRespTm float64) (string, error) {
	// estimate the mean of all servers response in m
	arr := mapToArray(servers)
	gMean := sum(arr) / float64(len(arr))
	meanDeviationArr := applyDeviation(arr, gMean)
	random := randFloatB(0, sumRespTm)
	step := 0.0
	for _, v := range meanDeviationArr {
		if random <= v.v+step {
			return v.k, nil
		}
		step += v.v
	}
	return "", errors.New("random not in range of values, fix needed in getForwardURLb")
}
