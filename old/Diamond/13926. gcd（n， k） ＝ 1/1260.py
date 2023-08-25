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

if __name__ == '__main__':
	vertex, edge, begin = inputline(int, split=True)
	graph = [[] * vertex]

	for i in range(edge):
		start, end = inputline(int, split=True)
		graph[start].append(end)
		graph[end].append(start)

	dfs(graph, begin)
	bfs(graph, begin)

def dfs(graph: list[list[int]], begin: int):
	print(begin)

def bfs(graph: list[list[int]], begin: int):
	print(begin)