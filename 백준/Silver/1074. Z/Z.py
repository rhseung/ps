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

def board(N: int, find: tuple[int]):
	if N == 0:
		return 0
	else:
		return (find[1] % 2) + (2 * (find[0] % 2)) + 4 * board(N - 1, (find[0] // 2, find[1] // 2))

if __name__ == '__main__':
	N, r, c = inputline(int, split=True)

	print(board(N, (r, c)))