from sys import stdin
from sys import setrecursionlimit
from math import *
from random import randint
from collections import Counter
from fractions import Fraction
def inputline(type, split=False):
	if split:
		return list(map(type, stdin.readline().strip().split()))
	else:
		return type(stdin.readline().strip())

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

def backtracking(n: int, i: int):
	if n == 0:
		print(i)
		return
	else:
		for p in range(10):
			if is_prime(i * 10 + p):
				backtracking(n - 1, i * 10 + p)

if __name__ == '__main__':
	n = inputline(int)

	backtracking(n - 1, 2)
	backtracking(n - 1, 3)
	backtracking(n - 1, 5)
	backtracking(n - 1, 7)
