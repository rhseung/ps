# BOJ 13729 - 1013 피보나치
import sys

def input() -> str:
    return sys.stdin.readline()

n = int(input().strip())
if n == 10**13:
    print(-1)
    exit()

def fib(n: int, mod: int) -> int:
    def fd(x: int) -> tuple[int, int]:
        if x == 0:
            return 0, 1

        a, b = fd(x >> 1)
        t = (2 * b - a) % mod
        c = (a * t) % mod
        d = (a * a + b * b) % mod

        if x & 1:
            return d, (c + d) % mod
        else:
            return c, d

    return fd(n)[0]

base_k = 3
mod_k = 10 ** 3
period_k = 15 * 10 ** 2

C: list[int] = []
f0, f1 = 0, 1
for i in range(period_k):
    val = f0
    f0, f1 = f1, (f0 + f1) % mod_k
    if val == n % mod_k:
        C.append(i)

for k in range(base_k + 1, 13 + 1):
    next_mod = 10 ** k
    period_curr = 15 * 10 ** (k - 1)

    C_next: list[int] = []
    period_prev = period_curr // 10
    add = period_prev

    target = n % next_mod
    for i in C:
        base_idx = i
        for m in range(10):
            idx = base_idx + m * add
            if fib(idx, next_mod) == target:
                C_next.append(idx)

    C = C_next
    if not C:
        break

if C:
    print(min(C))
else:
    print(-1)