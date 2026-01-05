# BOJ 9012 - 괄호
import sys
def input() -> str: return sys.stdin.readline().rstrip()

def valid(s: str) -> bool:
    L = []
    for c in s:
        if c == '(':
            L.append(c)
        elif L and L[-1] == '(':
            L.pop()
        else:
            return False

    return False if L else True

n = int(input())
for _ in range(n):
    print("YES" if valid(input()) else "NO")
