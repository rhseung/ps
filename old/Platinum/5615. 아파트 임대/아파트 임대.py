from sys import stdin
def inputline(): return stdin.readline().strip()

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

T = int(inputline())
count = 0
for _ in range(T):
	k = int(inputline())
	if is_prime(2*k + 1):
		count += 1
print(count)