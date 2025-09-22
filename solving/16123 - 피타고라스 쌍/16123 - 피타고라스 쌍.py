# BOJ 16123 - 피타고라스 쌍
import sys

sys.setrecursionlimit(1_000_000)
input = sys.stdin.readline

L = int(input())
if L <= 1:
    print(0 if L == 0 else 0 if L == 1 else 1)
    sys.exit(0)

lim = int(round(L ** (2.0 / 3.0))) + 10

mu = [0] * (lim + 1)
primes = []
mark = [False] * (lim + 1)
mu[1] = 1
for i in range(2, lim + 1):
    if not mark[i]:
        primes.append(i)
        mu[i] = -1
    for p in primes:
        v = i * p
        if v > lim:
            break
        mark[v] = True
        if i % p == 0:
            mu[v] = 0
            break
        else:
            mu[v] = -mu[i]

prefix = [0] * (lim + 1)
prefix[0] = 0
for i in range(1, lim + 1):
    prefix[i] = prefix[i - 1] + mu[i]

memo_M = {}


def M(n: int) -> int:
    if n <= lim:
        return prefix[n]
    if n in memo_M:
        return memo_M[n]
    res = 1
    i = 2
    while i <= n:
        q = n // i
        j = n // q
        res -= (j - i + 1) * M(q)
        i = j + 1
    memo_M[n] = res
    return res


def G(N: int) -> int:
    s = 0
    while N:
        s += M(N)
        N //= 2
    return s


ans = 0
s = 1
while s <= L:
    u = L // s
    v = L // (2 * s)
    if v == 0:
        s = L // u + 1
        continue

    next1 = L // u
    next2 = (L // (2 * v))
    t = next1 if next1 < next2 else next2

    mu_odd_sum = G(t) - G(s - 1)
    ans += mu_odd_sum * v * (u - v)
    s = t + 1

print(ans)
