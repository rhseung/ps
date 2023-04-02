from sys import stdin
from functools import lru_cache
from sys import setrecursionlimit
from math import gcd
from math import floor
from math import sqrt
from random import randint
def inputline(type_, split=False):
	if split == True:
		return list(map(type_, stdin.readline().strip().split()))
	else:
		return type_(stdin.readline().strip())

dp = [[0 for _ in range(2000)] for _ in range(2000)]

def separate(n: int, p: int) -> list[int]:
	ret = list[int]()
	while n > 0:
		ret.insert(0, n % p)
		n //= p
	return ret

def combination(n: int, r: int, m: int) -> int:    
	if r == 0 or n == r:
		return 1
	elif r == 1:
		return n % m
	elif dp[n][r] != 0:
		return dp[n][r]
	else:
		dp[n][r] = (combination(n-1, r-1, m) % m + combination(n-1, r, m) % m) % m
		return dp[n][r]

if __name__ == '__main__':
	# m, n, p = inputline(int, split=True)
	
	# m_s = separate(m, p)
	# n_s = separate(n, p)
	
	# ret = 1
	# for i in range(min(len(m_s), len(n_s))):
	# 	ret = (ret % p * combination(m_s[i], n_s[i], p) % p) % p
  
	# print(ret)
 
	for i in range(1, 10):
		for j in range(1, 10):
			print(f"{i}C{j} = {combination(i, j, 1000000007)}")