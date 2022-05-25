const multithreadWorkers = require('./multithreading')
const { kill }= require('process')
const cluster = require('cluster')

if (cluster.isMaster) {
	const multiprocessingWorkers = (nbJob, jobDifficulty) => new Promise((res, rej) => {
		// doesn't work, why?
		const timeout = setTimeout(() => {
			while(Object.keys(cluster.workers).length !== 0) {
				cluster.removeAllListeners(['online', 'message'])
				console.log(Object.keys(cluster.workers).length)
				childPid = cluster.workers[Object.keys(cluster.workers)[0]].process.pid
				kill(childPid, 'SIGKILL')
			}
			rej(new Error("timed out"))
		}, 4000)

		for (let i = 0; i < nbJob; i++) {
			const worker = cluster.fork({ workerId: i})
			console.log(`created worker ${worker.id}`)
		}

		cluster.on('online', (worker) => {
			worker.send(jobDifficulty)
			console.log(`sent job to worker ${worker.id}`)
		})

		cluster.on('message', (worker, msg) => {
			console.log(`job result received from worker ${worker.id}=${msg}`)
			worker.kill()
			console.log(`worker ${worker.id} killed`)
			console.log(cluster.workers)
			if (Object.keys(cluster.workers).length === 0) {
				clearTimeout(timeout)
				res()
			}
		})
	})

	const main = async () => {
		try {
			await multiprocessingWorkers(5, 1e9)
		} catch(e) {
			console.err(e)
		}
		console.log("out of this sht")
	}

	main()
} else {
	const { computeIntensiveTask } = require('./hardWork');
	process.on('message', (arg) => {
		process.send(computeIntensiveTask(1e20))
	})
}
