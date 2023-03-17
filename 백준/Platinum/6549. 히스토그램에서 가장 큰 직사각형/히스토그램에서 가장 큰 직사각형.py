from sys import stdin
from sys import setrecursionlimit
from functools import lru_cache as memoization
from collections import Counter
from collections import deque
setrecursionlimit(10 ** 4)
def inputline(): return stdin.readline().strip()

def surface(heights: list[int], start: int, end: int) -> int:
	try:
		if start == end: return heights[start]

		mid = (start + end) // 2
		left_surface = surface(heights, start, mid)
		right_surface = surface(heights, mid + 1, end)

		low, high, height = mid, mid, heights[mid]
		max_surface = height * 1

		# [4, 6] 에서 [5, 6]

		while True:
			if low == start:
				high += 1
				height = min(height, heights[high])
			elif high == end:
				low -= 1
				height = min(height, heights[low])
			elif heights[low - 1] <= heights[high + 1]:
				high += 1
				height = min(height, heights[high])
			elif heights[low - 1] > heights[high + 1]:
				low -= 1
				height = min(height, heights[low])

			new_surface = (high - low + 1) * height
			max_surface = max(max_surface, new_surface)

			if start == low and end == high: break

		# print(f"[{start}, {end}]: {left_surface} -> {max_surface} -> {right_surface}")
		return max(max_surface, left_surface, right_surface)

	except IndexError as e:
		print(f"[{start}, {end}]")

while True:
	x = inputline().split()

	if x[0] == "0": break

	n = int(x[0])
	arr = [] * n
	for e in x[1:]:
		arr.append(int(e))

	if len(arr) == 1:
		print(arr[0])
	else:
		print(surface(arr, 0, n - 1))