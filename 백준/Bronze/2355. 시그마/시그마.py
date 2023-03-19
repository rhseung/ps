from sys import stdin
from sys import setrecursionlimit
from math import *
from random import randint
from collections import Counter
def inputline(type, split=False):
	if split:
		return list(map(type, stdin.readline().strip().split()))
	else:
		return type(stdin.readline().strip())

def sum(a, b): return (a+b)*(b-a+1)//2

if __name__ == '__main__':
	a, b = inputline(int, split=True)

	if a > b: a, b = b, a

	print(sum(a, b))