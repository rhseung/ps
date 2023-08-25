from sys import stdin
from sys import setrecursionlimit
from functools import lru_cache as memoization
from collections import Counter
from collections import deque
setrecursionlimit(10 ** 4)
def inputline(): return stdin.readline().strip()

def surface(sizes: list[int], start: int, end: int) -> int:
	if start == end: return sizes[start]**2

	mid = (start + end) // 2
	low, high, height, width = mid, mid, sizes[mid], sizes[mid]
	max_surface = max(surface(sizes, start, mid), surface(sizes, mid + 1, end))

	while True:
		add = 0
		if low == start:
			high += 1
			add = sizes[high]
		elif high == end:
			low -= 1
			add = sizes[low]
		elif sizes[low - 1] <= sizes[high + 1]:
			high += 1
			add = sizes[high]
		elif sizes[low - 1] > sizes[high + 1]:
			low -= 1
			add = sizes[low]

		width += add
		height = min(height, add)
		max_surface = max(max_surface, width * height)

		if start == low and end == high: break

	return max_surface

n = int(input())
x = inputline().split()
arr = [] * n
for e in x:
	arr.append(int(e))

if len(arr) == 1:
	print(arr[0]**2)
else:
	print(surface(arr, 0, n - 1))