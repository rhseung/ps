# BOJ 15652 - N과 M (4)
import sys
def input() -> str: return sys.stdin.readline().rstrip()

n, m = map(int, input().split())

def dfs(cur: list[int]):
    if len(cur) == m:
        print(*cur)
        return

    for digit in range(cur[-1] if cur else 1, n + 1):
        dfs(cur + [digit])

dfs([])
