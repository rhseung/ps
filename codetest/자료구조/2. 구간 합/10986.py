import sys

input = sys.stdin.readline

size, mod = map(int, input().split())
arr = list(map(int, input().split()))

cum_mod_arr = [arr[0] % mod]
for i in range(1, size):
	cum_mod_arr.append((arr[i] + cum_mod_arr[i - 1]) % mod)

def combination2(x):
	return x * (x - 1) // 2

count = 0
counts = [0] * mod
for e in cum_mod_arr:
	counts[e] += 1

for freq in counts:
	count += combination2(freq)

# idea: 이렇게 하면 처음부터의
#  (cum_mod_arr[j] - cum_mod_arr[i] == 0일 때, i - 1 == -1 인 경우, 즉 i 없이 j 혼자서 나누어 떨어지는)
#  누적합을 구하는 경우가 무시됨, 처음부터의 합이 나누어 떨어지는 경우는 `cum_mod_arr`에서 0인 값의 경우임
print(count + counts[0])
