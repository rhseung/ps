from sys import stdin
from sys import setrecursionlimit
from functools import lru_cache as memoization
from collections import Counter
from collections import deque
setrecursionlimit(10 ** 3)
def inputline(): return stdin.readline().strip()

white, blue = 0, 0

class Pos:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def __str__(self):
		return f"(x={self.x}, y={self.y})"

def check_status(paper: list[list[int]], start, end):
	s = 0
	for i in range(start.x, end.x):
		for j in range(start.y, end.y):
			s += paper[i][j]

	if s == 0:
		return 0
	elif s == (end.y - start.y) * (end.x - start.x):
		return 1
	else:
		return -1

def square(paper: list[list[int]], start, end):
	global white, blue

	status = check_status(paper, start, end)

	if status == 0:
		white += 1
	elif status == 1:
		blue += 1
	else:
		center = Pos((start.x + end.x) // 2, (start.y + end.y) // 2)
		# print(f"{start} - {end}")
		# print(f"\tleftup  : {start} - {center}")
		# print(f"\trightup : {(center.x, end.x)} - {(start.y, center.y)}")
		# print(f"\tleftdow : {(start.x, center.x)} - {(center.y, end.y)}")
		# print(f"\trightdo : {(center.x, end.x)} - {(center.y, end.y)}")

		square(paper, start, center)   # left up
		square(paper, Pos(center.x, start.y), Pos(end.x, center.y))    # right up
		square(paper, Pos(start.x, center.y), Pos(center.x, end.y))    # left down
		square(paper, Pos(center.x, center.y), Pos(end.x, end.y))  # right down

def main():
	n = int(input())
	paper = [[0] * n] * n

	for i in range(n):
		paper[i] = list(map(int, inputline().split()))

	square(paper, Pos(0, 0), Pos(n, n))
	print(white)
	print(blue)

main()
