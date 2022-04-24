package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"math/rand"
	"os"
	"os/signal"
	"strings"
	"syscall"
	"time"
)

const (
	METRIC_HEADER string = "EXECUTION-TIME"
)

func main() {
	var err error
	// cancel all go routines on processus stop
	ctx, cancelfunc := context.WithCancel(context.Background())
	c := make(chan os.Signal)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)
	go func() {
		<-c
		cancelfunc()
		os.Exit(1)
	}()

	// seed random
	rand.Seed(time.Now().UnixNano())

	// startup flags
	configUrl := flag.String("f", "loadbalancer.conf", "Path of backends config file")
	port := flag.Int("p", 80, "Port of web server")
	flag.Parse()

	// parse config files, get string[]
	content, err := os.ReadFile(*configUrl)
	if err != nil {
		log.Fatal(fmt.Errorf("failed to read configuration file %v", err))
	}
	confLines := strings.Split(string(content), "\n")
	// config syntax check
	i := 0
	for i < len(confLines) {
		if url == "" {
			confLines = remove(confLines, i)
			continue
		}
		if !strings.HasPrefix(url, "http://") {
			log.Fatal("URLs in config file should start with http://")
		}
		i++
	}
	// start balancers (blocking)
	err = loadBalance(ctx, confLines, *port)
	if err != nil {
		log.Fatal(fmt.Errorf("balancers failed %v", err))
	}

	log.Printf("System shuting down...")
	wg.Wait()
	log.Printf("(づ￣ ³￣)づ byebye!")
}
