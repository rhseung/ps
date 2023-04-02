from sys import stdin
from sys import setrecursionlimit
from math import gcd
from math import floor
from math import sqrt
from random import randint
def inputline(type_, **kwargs):
	if 'split' in kwargs and kwargs['split']:
		return list(map(type_, stdin.readline().strip().split()))
	else:
		return type_(stdin.readline().strip())

def phi(n):
	r = n
	i = 2
	while i * i <= n:
		if n % i == 0:
			r -= r // i
			while n % i == 0:
				n //= i
		i += 1

	if n > 1:
		r -= r // n

	return r

if __name__ == '__main__':
	n = inputline(int)
	divisors = []

	i = 1
	while i * i <= n:
		if n % i == 0:
			divisors.append(i)
		i += 1

	l = len(divisors)
	for j in range(l):
		divisors.append(n // divisors[j])

	for d in set(divisors):
		if d * phi(d) == n:
			print(d)
			exit()

	print(-1)
	exit()