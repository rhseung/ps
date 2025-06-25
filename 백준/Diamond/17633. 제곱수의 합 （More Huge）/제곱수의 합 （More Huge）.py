from sys import stdin
from sys import setrecursionlimit
from math import gcd
from math import floor
from math import sqrt
from math import isqrt
from random import randint
from collections import Counter
def inputline(): return stdin.readline().strip()

def is_square(n: int) -> bool:
	return n == isqrt(n) ** 2

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

def main():
	n = int(inputline())
	factors = Counter(get_factors(n))

	# print(factors)

	if is_square(n):
		print(1)
		return

	flag = True
	for key, value in factors.items():
		if key % 4 == 3:
			if value % 2 == 1:
				flag = False
	if flag:
		print(2)
		return

	tmp = n
	while tmp % 4 == 0:
		tmp //= 4
	if tmp % 8 != 7:
		print(3)
		return

	print(4)
	return

main()