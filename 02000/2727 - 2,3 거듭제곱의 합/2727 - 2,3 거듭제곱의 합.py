# BOJ 2727 - 2,3 거듭제곱의 합
import sys

input = sys.stdin.readline


def decompose(n: int):
    a = 0
    terms = []
    while n > 0:
        while n % 2 == 0:
            a += 1
            n //= 2
        r = 1
        b = 0
        while r * 3 <= n:
            r *= 3
            b += 1
        n -= r
        terms.append((a, b))
    return terms


t = int(input())
for _ in range(t):
    n = int(input())
    ans = decompose(n)
    print(len(ans))
    for a, b in ans:
        print(a, b)
