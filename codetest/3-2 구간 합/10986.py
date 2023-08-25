import sys
from collections import Counter

input = sys.stdin.readline

size, mod = map(int, input().split())
arr = list(map(int, input().split()))

cum_arr = [arr[0] % mod]
for i in range(1, size):
	cum_arr.append((arr[i] + cum_arr[i - 1]) % mod)


# 1 2 3 1 2
# 1 0 0 1 0
# idea: 0의 개수는 처음부터 지금까지의 합이 해당되는 구간이 되는 경우를 의미한다.

def naive():
	count = 0
	for i in range(size):
		for j in range(i, size):
			
			# cum_arr[j] - (0 if i == 0 else cum_arr[i - 1]) == 0
			# <=> cum_arr[j] == (0 if i == 0 else cum_arr[i - 1])
			# idea: 나머지가 같은 쌍 개수 구하기 -> 쌍은 Combination(개수, 2) 개
			if cum_arr[j] == (0 if i == 0 else cum_arr[i - 1]):
				# print(i, j)
				count += 1


def c2(x):
	return x * (x - 1) // 2


count = 0
counts = Counter(cum_arr)
for key, freq in counts.items():
	# idea: 이렇게 하면 처음부터의 (i - 1 == -1 인 경우) 누적합을 구하는 경우가 무시됨
	#  - 처음부터의 합이 나누어 떨어지는 경우는 `cum_arr`이 0인 값의 경우임
	count += c2(freq)

print(count + counts[0])
