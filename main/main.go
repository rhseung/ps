package main

import (
	"fmt"
)

func main() {
	const N int = 100_000
	var n int
	var tmp int
	var D [N]int

	fmt.Scan(&n)
	fmt.Scan(&D[0])
	max_v := D[0]

	for i := 1; i < n; i++ {
		fmt.Scan(&tmp)

		D[i] = max(D[i-1], 0) + tmp
		max_v = max(max_v, D[i])
	}

	fmt.Println(max_v)
}
