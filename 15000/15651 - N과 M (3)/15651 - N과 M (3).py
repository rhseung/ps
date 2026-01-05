# BOJ 15651 - N과 M (3)
import sys
def input() -> str: return sys.stdin.readline().rstrip()

n, m = map(int, input().split())

def dfs(cur: list[int]):
    if len(cur) == m:
        print(*cur)
        return

    for digit in range(1, n + 1):
        dfs(cur + [digit])

dfs([])