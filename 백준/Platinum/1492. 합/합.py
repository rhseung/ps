__problem__ = 'https://boj.kr/1492', '합'

import sys

input = sys.stdin.readline

n, k = map(int, input().split())
m = 1_000_000_007

# sum n^k = a * sum n(n-1)(n-2)...(n-(k-1)) + b * sum n(n-1)(n-2)...(n-(k-2)) + ...

#   k-1k-2k-3k-4k-5=> l
#    0  1  2  3  4 => k-l-1
# 0  1
# 1  1  1
# 2  1  3  1
# 3  1  6  7  1
# 4  1  10 25 15 1
# |
# k

# dp[i-1][j-1] * ((i+1)-j) + dp[i-1][j] = dp[i][j]
dp = [[0 for _ in range(k)] for _ in range(k)]
def coeff(k, l, mod):
    if dp[k][l] != 0:
        return dp[k][l]
    elif l == 0:
        return 1
    elif k == l:
        return 1
    else:
        dp[k][l] = ((coeff(k-1, l-1, mod) * ((k+1 - l) % mod)) % mod + coeff(k-1, l, mod)) % mod
        return dp[k][l]

# sum n(n-1)(n-2)...(n-l) = P(N+1, l+2)/(l+2)
def permutation(n, l, mod):
    ret = 1
    for i in range(l):
        ret = (ret * ((n - i) % mod)) % mod

    return ret

# b^(p-1) mod p = 1
# b^(p-2) mod p = 1/b
# a/b mod p = (a mod p) * (1/b mod p) mod p = (a mod p) * (b^(p-2) mod p) mod p
def fast_pow(x, p, mod):
    if p == 1:
        return x % mod

    half = fast_pow(x, p // 2, mod)
    return ((half * half) % mod * (x % mod if p % 2 == 1 else 1)) % mod

def div(a, b, mod):
    return ((a % mod) * (fast_pow(b, mod - 2, mod))) % mod

C = [coeff(k - 1, l, m) for l in range(k)]
V = [(C[i] * div(permutation(n + 1, k + 1 - i, m), k + 1 - i, m)) % m for i in range(k)]

s = 0
for v in V:
    s = (s + v) % m

print(s)
