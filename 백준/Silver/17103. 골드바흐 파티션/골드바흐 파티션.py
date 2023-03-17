import math
from sys import stdin
from sys import setrecursionlimit
from functools import lru_cache as memoization
from collections import Counter
from collections import deque

setrecursionlimit(10 ** 4)

def inputline(): return stdin.readline().strip()

def make_sieve(x):
	sieve = [True] * (x + 1)

	for i in range(2, x + 1):
		if not sieve[i]: continue

		for j in range(2*i, x + 1, i):
			sieve[j] = False

	return sieve

def goldbach(x):
	primes = make_sieve(x)
	c = 0
	for n in range(2, math.ceil(x / 2) + 1):
		if primes[n] and primes[x - n]:
			c += 1

	return c

def main():
	n = int(inputline())
	for i in range(n):
		x = int(inputline())
		print(goldbach(x))

main()