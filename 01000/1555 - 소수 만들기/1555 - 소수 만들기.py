# BOJ 1555 - 소수 만들기
import sys
sys.setrecursionlimit(10000)

def input() -> str:
    return sys.stdin.readline().rstrip()

def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

n = int(input())
A = list(map(int, input().split()))

l = 1 << n
DP = [set() for _ in range(l)]

for i in range(n):
    DP[1 << i] = {A[i]}

for mask in range(1, l):
    s = (mask - 1) & mask

    if s == 0:
        continue

    R = set()
    while s:
        left = DP[s]
        right = DP[mask ^ s]
        if left and right:
            for a in left:
                for b in right:
                    R.add(a + b)
                    R.add(a - b)
                    R.add(a * b)
                    if a > 0 and b > 0:
                        R.add(a // b)
        s = (s - 1) & mask

    DP[mask] = R

ALL = DP[l - 1]
P = [v for v in ALL if is_prime(v)]
if not P:
    print(-1)
else:
    print(min(P))
    print(max(P))