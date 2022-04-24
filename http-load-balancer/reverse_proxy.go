package main

import (
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"strconv"
)

// NewProxy takes target host and creates a reverse proxy
func NewProxy(targetHost string) (*httputil.ReverseProxy, error) {
	url, err := url.Parse(targetHost)
	if err != nil {
		return nil, err
	}

	proxy := httputil.NewSingleHostReverseProxy(url)

	originalDirector := proxy.Director
	proxy.Director = func(req *http.Request) {
		originalDirector(req)
		req.Header.Set("X-Forward-Host", req.Header.Get("Host"))
		req.Host = req.URL.Host
	}

	proxy.ModifyResponse = modifyResponse(targetHost)
	proxy.ErrorHandler = errorHandler(targetHost)
	return proxy, nil
}

func errorHandler(serverURL string) func(http.ResponseWriter, *http.Request, error) {
	return func(w http.ResponseWriter, req *http.Request, err error) {
		log.Printf("Got error while modifying response: %v from %s", err, serverURL)
	}
}

func modifyResponse(serverURL string) func(*http.Response) error {
	return func(resp *http.Response) error {
		metric := resp.Header.Get(METRIC_HEADER)
		i, err := strconv.ParseInt(metric, 10, 32)
		if err != nil {
			// failed to parse metrics, what TODO ?
			log.Printf("Failed to parse metrics from %s", serverURL)
			return nil
		}
		for _, balancer := range balancers {
			balancer <- ResponseTime{r: float64(i), url: serverURL}
		}
		return nil
	}
}

func ProxyRequestHandler(proxy *httputil.ReverseProxy) func(http.ResponseWriter, *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		proxy.ServeHTTP(w, r)
	}
}
