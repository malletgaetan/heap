const { kill } = require('process')
const cluster = require('cluster')

if (cluster.isPrimary) {
	const worker = cluster.fork()
	cluster.on('message', (worker, msg) => {
		console.log(msg)
	})

	setTimeout(() => kill(worker.process.pid, 'SIGKILL'), 10000)

} else {
	for(let i = 0; i <= 1e20; i++) {}
}
