const {
  Worker, isMainThread, parentPort, workerData
} = require('worker_threads');

if (isMainThread) {
	module.exports = async (nbJob, jobDifficulty) => {
		const doJobAsync = () => new Promise((res, rej) => {
			const worker = new Worker(__filename, { workerData: jobDifficulty })
			worker.on('message', res)
			worker.on('error', rej)
			worker.on('exit', (code) => {
				if (code !== 0)
					rej(new Error(`Worker stopped with exit code ${code}`))
			})
		})

		return new Promise(async (res, rej) => {
			const jobs = []
			for(let i = 0; i < nbJob; i++){
				jobs.push(doJobAsync())
			}
			try {
				await Promise.all(jobs)
				res()
			} catch(e) {
				rej(e)
			}
		})
	}
} else {
	const { computeIntensiveTask } = require('./hardWork');
	const jobDifficulty = workerData
	parentPort.postMessage(computeIntensiveTask(jobDifficulty));
}
