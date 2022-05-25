const computeIntensiveTask = (objective) => {
	let counter = 0
	for(let i = 0; i < objective; i++){
		counter++
	}
	return counter
}

module.exports = { computeIntensiveTask }
