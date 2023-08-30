import sys
input = sys.stdin.readline

id_count = int(input())
require = int(input())
ids = list(map(int, input().split()))

ids.sort()
left, right = 0, len(ids) - 1
count = 0

while left < right:
	key = ids[left] + ids[right]
	
	if key < require:
		left += 1
	elif key > require:
		right -= 1
	else:
		count += 1
		left += 1

print(count)
