import sys
input = sys.stdin.readline


def sum_range(a: int, b: int) -> int:
	"""
	>>> sum_range(1, 10)
	55
	>>> sum_range(3, 7)
	25
	"""
	
	return (a + b) * (b - a + 1) // 2

n = int(input())
count = 0
left, right = 1, 1

while left <= right:
	key = sum_range(left, right)
	
	if key < n:
		right += 1
	elif key == n:
		# print(left, right)
		count += 1
		right += 1
	else:
		left += 1

print(count)
