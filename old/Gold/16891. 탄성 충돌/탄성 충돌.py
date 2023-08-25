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

if __name__ == '__main__':
	n = inputline(int)
	print(floor(pi/atan(1/n) - 0.0001))
