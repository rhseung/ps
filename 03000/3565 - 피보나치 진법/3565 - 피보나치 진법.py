# BOJ 3565 - 피보나치 진법
import sys
input = sys.stdin.readline

N = int(input().strip())

if N == 0:
    print(0)
    sys.exit(0)

MAX_K = 100

a = [0] * (MAX_K + 1)
b = [0] * (MAX_K + 1)

a[0] = 1
a[1] = 2
b[0] = 0
b[1] = 1
for k in range(2, MAX_K + 1):
    a[k] = a[k-1] + a[k-2]
    b[k] = b[k-1] + (a[k-2] + b[k-2])

def prefix_sum_ones(k: int, m: int) -> int:
    if m <= 0 or k == 0:
        return 0
    if k == 1:
        return 0 if m == 1 else 1

    first_block = a[k-1]
    if m <= first_block:
        return prefix_sum_ones(k-1, m)

    rest = m - first_block
    return b[k-1] + rest + prefix_sum_ones(k-2, rest)

def prefix_ones_of_jth(k: int, j: int, t: int) -> int:
    if t <= 0 or k == 0:
        return 0
    if k == 1:
        s = "0" if j == 0 else "1"
        return s[:t].count('1')

    first_block = a[k-1]
    if j < first_block:
        return prefix_ones_of_jth(k-1, j, t-1)
    else:
        j2 = j - first_block
        if t == 1:
            return 1
        if t == 2:
            return 1
        return 1 + prefix_ones_of_jth(k-2, j2, t-2)

ans = 0
remain = N

if remain > 0:
    take = min(1, remain)
    ans += take
    remain -= take

L = 2
while remain > 0:
    k = L - 2
    cnt = a[k] if L >= 2 else 1
    block_len = cnt * L
    if remain >= block_len:
        ans += cnt + b[k]
        remain -= block_len
        L += 1
        continue

    m = remain // L
    r = remain % L
    if m > 0:
        ans += m
        ans += prefix_sum_ones(k, m)
    if r > 0:
        if r == 1:
            ans += 1
        elif r == 2:
            ans += 1
        else:
            ans += 1 + prefix_ones_of_jth(k, m, r-2)
    break

print(ans)