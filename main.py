from sys import stdin
from functools import lru_cache
from sys import setrecursionlimit
from math import gcd
from math import floor
from math import sqrt
from random import randint
def inputstream(type_, split=False):
	if split == True:
		return list(map(type_, stdin.readline().strip().split()))
	else:
		return type_(stdin.readline().strip())

def phi(n):
	if n == 1:
		return 1
		
	result = n
	for i in range(2, int(n ** 0.5) + 1):
		if n % i == 0:
			while n % i == 0:
				n //= i
			result -= result // i
	if n > 1:
		result -= result // n
	return result

def pow(n, p, mod):
	if p == 0:
		return 1
	else:
		x = (pow(n, p // 2, mod) % mod * pow(n, p - p // 2, mod) % mod) % mod
		if p % 2 == 1: x = (x * n) % mod
		return x

# f(n, mod) = n ** f(n, mod % φ(mod))
def f(n, mod):
    print(mod)
    
    if mod == 1 or n == 1: return 1
    else: return pow(n, f(n, mod % phi(mod)) % mod, mod)

if __name__ == '__main__':
    T = inputstream(int)
    for i in range(T):
        n, mod = inputstream(int, split=True)
        print(f(n, mod))