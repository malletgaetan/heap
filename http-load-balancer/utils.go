package main

import (
	"math/rand"
)

type MapValue struct {
	v float64
	k string
}

// sort of fake mean calculation, but tends to the mean
// return the value to be added to the 'fake'mean so it tend to 'real'mean
func scaledMean(value float64, mean float64, nNb float64) float64 {
	if value != mean {
		return (value - mean) / nNb
	}
	return mean
}

// random float64 beetween min and max
func randFloatB(min float64, max float64) float64 {
	return min + rand.Float64()*(max-min)
}

// remove an element from a slice
func remove(slice []string, s int) []string {
	return append(slice[:s], slice[s+1:]...)
}

// transform map MapValue array
func mapToArray(servers map[string]float64) (res []MapValue) {
	for k, v := range servers {
		res = append(res, MapValue{k: k, v: v})
	}
	return res
}

// sum of array of MapValue by value
func sum(arr []MapValue) float64 {
	res := 0.0
	for _, v := range arr {
		res += v.v
	}
	return res
}

// example
// arr = [{k:"fastest_server", v: 200}, {k:"fast_server", v: 400}, {k:"slow_server", v: 500}, {k:"slowest_server", v: 700}]
// become
// [{k:"fastest_server", v: 650}, {k:"fast_server", v: 550}, {k:"slow_server", v: 450}, {k:"slowest_server", v: 250}]
// so the slowest server become the least probable solution for a random number in the range [0..sum(arr)]
func applyDeviation(arr []MapValue, mean float64) []MapValue {
	for i := 0; i < len(arr); i++ {
		arr[i].v += (mean - arr[i].v) * 2.0
	}
	return arr
}
