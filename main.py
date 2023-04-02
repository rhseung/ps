from sys import stdin
from sys import setrecursionlimit
from math import gcd
from math import floor
from math import sqrt
from random import randint
def inputline(type_, split=False):
	if split:
		return list(map(type_, stdin.readline().strip().split()))
	else:
		return type_(stdin.readline().strip())

if __name__ == '__main__':
	N = inputline(int)
	numbers = inputline(int, split=True)
	numbers.sort()

	if N == 1:
		print(sum(numbers[0:5]))
		exit()

	a = [min(numbers[0], numbers[5]), min(numbers[1], numbers[4]), min(numbers[2], numbers[3])]
	a1, a2, a3 = min(a[0], a[1], a[2]), min(a[0] + a[1], a[1] + a[2], a[2] + a[0]), a[0] + a[1] + a[2]
	n1, n2, n3 = 4*(N-1)*(N-2)+(N-2)**2, 8*N-12, 4

	print(a1*n1 + a2*n2 + a3*n3)