# HTTP Load Balancer

## Specifications

- http servers should always return time taken to proceed request in headers as EXECUTION_TIME in ms
- this load balancer choose where to balance regarding of the response time. > ResponseTime, < chances to receive requests

## Getting started

1. create a file at in root folder of load balance, <file_name>
2. add every address the load balance need to access, one row for one server, with http:// format
3. Start load balancer!
```go
// in terminal, at the root of load balancer, type =>
go build
```
then
```bash
./http-load-balancer -f <file_name> -p <load_balancer_port>
```

And your good to go (ノ^∇^)

## COULDDO

- [ ] TLS support
- [ ] support comments in conf file
- [ ] requests retry
- [ ] servers health checks
