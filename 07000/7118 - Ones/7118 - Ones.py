# BOJ 7118 - Ones
import sys
input = sys.stdin.readline

def v_p(x: int, p: int) -> int:
    cnt = 0
    while x % p == 0:
        x //= p
        cnt += 1
    return cnt

p, n = map(int, input().split())

if p % 2 == 0 or n % 2 == 1:
    v2 = 0
else:
    # p: odd, n: even => v2 = v2(p+1) + v2(n) - 1
    v2 = v_p(p + 1, 2) + v_p(n, 2) - 1

r = p % 3
if r == 0:
    v3 = 0
elif r == 1:
    v3 = v_p(n, 3)
else:
    if n % 2 == 1:
        v3 = 0
    else:
        v3 = v_p(p + 1, 3) + v_p(n, 3)

print(v2, v3)