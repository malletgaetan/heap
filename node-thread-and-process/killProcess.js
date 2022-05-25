const { kill } = require('process')
const cluster = require('cluster')

if (cluster.isPrimary) {
  // Fork workers.
	const worker = cluster.fork()
	cluster.on('message', (worker, msg) => {
		console.log(msg)
	})

	setTimeout(() => kill(worker.process.pid, 'SIGKILL'), 10000)

} else {
  // Workers can share any TCP connection. In this case, it is an HTTP server.
	// setTimeout(() => console.log("ntm"), 20000)
	for(let i = 0; i <= 1e20; i++) {}
}
