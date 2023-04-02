from math import *
from random import randint
from collections import Counter

class prime:
	@staticmethod
	def mul(a: int, b: int, m: int):
		return a * b % m

	@staticmethod
	def pow(a: int, b: int, m: int) -> int:
		ret = 1

		while b >= 1:
			if b % 2 == 1:
				ret = prime.mul(ret, a, m)
			a = prime.mul(a, a, m)
			b //= 2

		return ret

	@staticmethod
	def miller_rabin(n: int, a: int) -> bool:
		s = 0
		tmp = n - 1
		while tmp % 2 == 0:
			tmp //= 2
			s += 1
		d = tmp

		p = prime.pow(a, d, n)
		if p == 1 or p == n - 1:
			return True

		x = prime.pow(a, d, n)
		for r in range(s):
			if x == n - 1:
				return True
			x = prime.pow(x, 2, n)

		return False

	@staticmethod
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

			is_probable_prime = prime.miller_rabin(n, a)
			if not is_probable_prime:
				return False

		return True

	@staticmethod
	def pollard_rho(n: int, i: int) -> int:
		if prime.is_prime(n):
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
			return prime.pollard_rho(n, i + 2)
		elif prime.is_prime(d):
			return d
		else:
			return prime.pollard_rho(d, 1)

	@staticmethod
	def factorization(n: int) -> list[int]:
		factors = []

		while n > 1:
			factor = prime.pollard_rho(n, 1)
			factors.append(factor)
			n //= factor

		factors.sort()
		return factors

	@staticmethod
	def count_divisions(n: int):
		factors = Counter(prime.factorization(n))
		count = 1
		for p in factors:
			count *= (p + 1)
		return count

	@staticmethod
	def count_disjoints(n: int):
		factors = set(prime.factorization(n))
		for p in factors:
			n = (n // p) * (p - 1)
		return n

if __name__ == "__main__":
	n = int(input())
	print("약수 개수", prime.count_divisions(n))
	print("서로소 개수", prime.count_disjoints(n))
	print("소인수 분해", prime.factorization(n))
