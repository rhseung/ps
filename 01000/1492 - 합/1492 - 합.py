# BOJ 1492 - 합
import sys
def input() -> str: return sys.stdin.readline()

n, k = map(int, input().split())
m = 1_000_000_007

# 애초에 sum n^k (2 <= k <= 3) 까지 손으로 증명할 때도 이렇게 함
# sum n^2 = sum n(n-1) + sum n
# sum n^3 = sum n(n-1)(n-2) + 3 * sum n(n-1) + sum n
# ...
# sum n^k = C0 * sum n(n-1)(n-2)...(n-(k-1)) + C1 * sum n(n-1)...(n-(k-2)) + C2 * ...

# 1
# 1  1
# 1  3  1
# 1  6  7  1
# 1  10 25 15 1
# C[i][j] = C[i - 1][j] + ((i + 1) - j) * C[i - 1][j - 1]

# sum n(n-1)(n-2)...(n-l) from n=0 to N = (N+1)N(N-1)...(N-l)/(l+2)
def sigma(l: int, to: int) -> int:
    ret = 1
    for x in range(to - l, to + 2):
        ret *= x
        ret %= m
    ret *= pow(l + 2, -1, m)

    return ret

C = [[0 for _ in range(k)] for _ in range(k)]

C[0][0] = 1
if k > 1:
    C[1][0] = 1
    C[1][1] = 1

for i in range(2, k):
    for j in range(i + 1):
        if j == 0:
            C[i][j] = 1
        else:
            C[i][j] = (C[i - 1][j] + ((i + 1) - j) * C[i - 1][j - 1] % m) % m

ans = 0
for i in range(k):
    ans += C[k - 1][i] * sigma(k - 1 - i, n)
    ans %= m

print(ans)
