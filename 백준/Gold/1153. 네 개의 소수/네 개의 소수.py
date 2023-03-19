from sys import stdin
from sys import setrecursionlimit
from math import *
from random import randint
from collections import Counter
def inputline(type, split=False):
	if split:
		return list(map(type, stdin.readline().strip().split()))
	else:
		return type(stdin.readline().strip())

size = 1_000_000
primes = [True] * (size + 1)

def make_sieve(x):
	for i in range(2, x + 1):
		if not primes[i]: continue

		for j in range(2*i, x + 1, i):
			primes[j] = False

def goldbach(x):
	for n in range(2, ceil(x / 2) + 1):
		if primes[n] and primes[x - n]:
			return n, x - n

	print(-1)
	exit()

if __name__ == '__main__':
	n = inputline(int)
	make_sieve(n)

	if n % 2 == 1:
		result = (2, 3) + goldbach(n - 5)
	else:
		result = (2, 2) + goldbach(n - 4)

	print(*result)