import sys

input = sys.stdin.readline
MOD = 1_000_000_007

n = int(input())


def fib(n: int):
    if n == 0:
        return 0, 1
    a, b = fib(n >> 1)
    c = (a * ((b << 1) - a)) % MOD
    d = (a * a + b * b) % MOD
    if n & 1:
        return d % MOD, (c + d) % MOD
    else:
        return c % MOD, d % MOD


DP = {0: 0, 1: 1}


def phi(n: int) -> int:
    if n in DP:
        return DP[n]

    res = n * (n + 1) // 2
    l = 2
    while l <= n:
        q = n // l
        r = n // q
        res -= (r - l + 1) * phi(q)
        l = r + 1
    DP[n] = res
    return res


ans = 0
l = 1
while l <= n:
    q = n // l
    r = n // q

    frp2 = fib(r + 2)[0]
    flp1 = fib(l + 1)[0]
    sum_f = (frp2 - flp1) % MOD

    aq = (2 * phi(q) - 1) % MOD

    ans = (ans + sum_f * aq) % MOD
    l = r + 1

print(ans % MOD)
