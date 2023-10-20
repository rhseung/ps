import sys
from math import sqrt

problem_url = "https://boj.kr/2023"
problem_name = "신비한 소수"
input = sys.stdin.readline

n = int(input())

primes = [2, 3, 5, 7]

def is_prime(number):
	i = 2
	while i*i <= number:
		if number % i == 0:
			return False
		
		i += 1
	
	return True

def dfs(k):
	if k >= 10**(n-1):
		print(k)
		return
	
	number = k
	for adder in range(1, 10):
		number = k * 10 + adder
		if is_prime(number):
			dfs(number)

for k in primes:
	dfs(k)
