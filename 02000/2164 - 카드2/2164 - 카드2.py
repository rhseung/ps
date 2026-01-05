# BOJ 2164 - 카드2
import sys
from collections import deque


def input() -> str: return sys.stdin.readline().rstrip()

n = int(input())
L = deque(range(1, n + 1))

while len(L) > 1:
    L.popleft()
    L.append(L.popleft())

print(L[0])