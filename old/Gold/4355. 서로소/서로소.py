from sys import stdin
from sys import setrecursionlimit
from math import *
from random import randint
from collections import Counter
from fractions import Fraction
def inputline(type_, **kwargs):
	if 'split' in kwargs and kwargs['split']:
		return list(map(type_, stdin.readline().strip().split()))
	else:
		return type_(stdin.readline().strip())

def powmod(a: int, b: int, m: int) -> int:
	ret = 1

	while b >= 1:
		if b % 2 == 1:
			ret = (ret * a) % m
		a = (a * a) % m
		b //= 2

	return ret

def miller_rabin(n: int, a: int) -> bool:
	s = 0
	tmp = n - 1
	while tmp % 2 == 0:
		tmp //= 2
		s += 1
	d = tmp

	p = powmod(a, d, n)
	if p == 1 or p == n - 1:
		return True

	x = powmod(a, d, n)
	for r in range(s):
		if x == n - 1:
			return True
		x = powmod(x, 2, n)

	return False

def is_prime(n: int) -> bool:
	if n == 1:
		return False
	elif n == 2:
		return True
	elif n % 2 == 0:
		return False

	alist = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
	for a in alist:
		if n == a:
			return True

		is_probable_prime = miller_rabin(n, a)
		if not is_probable_prime:
			return False

	return True

def pollard_rho(n: int, i: int) -> int:
	if is_prime(n):
		return n
	elif n % 2 == 0:
		return 2

	g = lambda x: (x ** 2 + i) % n
	x = randint(1, floor(sqrt(n - 1))) ** 2 + 1
	y = x
	d = 1

	while d == 1:
		x = g(x)
		y = g(g(y))
		d = gcd(abs(x - y), n)

	if d == n:
		return pollard_rho(n, i + 2)
	elif is_prime(d):
		return d
	else:
		return pollard_rho(d, 1)

def get_factors(n):
	factors = []

	while n > 1:
		factor = pollard_rho(n, 1)
		factors.append(factor)
		n //= factor

	factors.sort()
	return factors

def do_case(n):
	factors = set(get_factors(n))
	for f in factors:
		n = (n // f) * (f - 1)
	print(n)

while True:
	x = int(inputline(int))
	if x == 0:
		exit()
	if x == 1:
		print(0)
	else:
		do_case(x)