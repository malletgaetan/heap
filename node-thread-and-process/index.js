const multithreadWorkers = require('./multithreading')
const { kill }= require('process')
const cluster = require('cluster')


const multiprocessingWorkers = (nbJob, jobDifficulty, timeout) => () => new Promise((res, rej) => {
	const timeAOUT = setTimeout(() => {
		for (const id in cluster.workers) {
			console.log('Killing remaining processes')
			let process_id = cluster.workers[id].process.pid
			kill(process_id, 'SIGKILL')
		}
		cluster.removeAllListeners(['online', 'message', 'exit'])
		rej(new Error('timed out'))
	}, (timeout || 30) * 1000)

	for (let i = 0; i < nbJob; i++) {
		const worker = cluster.fork({ workerId: i})
		console.log(`created worker ${worker.id}`)
	}

	cluster.on('online', (worker) => {
		worker.send(jobDifficulty)
		console.log(`sent job to worker ${worker.id}`)
	})

	cluster.on('message', (worker) => {
		worker.kill()
		console.log(`worker ${worker.id} killed`)
		if (Object.keys(cluster.workers).length === 0) {
			res()
		}
	})

	cluster.on('exit', () => {
		if (Object.keys(cluster.workers).length === 0) {
			clearTimeout(timeAOUT)
		}
	})
})

const time = async (fn) => {
	const before = Date.now()
	await fn()
	const after = Date.now()
	return (after - before)
}

const main = async () => {
	const jobDifficulty = 1e10
	// both will run in parallel anyway, process cool for isolation, threads simpler
	try {
		const pTime = await time(multiprocessingWorkers(20, jobDifficulty))
		const tTime = await time(multithreadWorkers(20, jobDifficulty))
		console.log(`multiprocessing took ${pTime}ms`)
		console.log(`multithreading took ${tTime}ms`)
	} catch(e) {
		console.error(e)
	}
}

if (cluster.isMaster) {
	main()
} else {
	// start worker
	const { computeIntensiveTask } = require('./hardWork');
	process.on('message', (arg) => {
		process.send(computeIntensiveTask(arg))
		process.removeAllListeners(['message'])
		process.exit(0)
	})
}
