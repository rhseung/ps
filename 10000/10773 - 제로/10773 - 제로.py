# BOJ 10773 - 제로
import sys
def input() -> str: return sys.stdin.readline().rstrip()

n = int(input())
L = []

for _ in range(n):
    x = int(input())
    if x == 0:
        L.pop()
    else:
        L.append(x)

print(sum(L))