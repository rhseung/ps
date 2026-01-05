# BOJ 15649 - N과 M (1)
import sys
def input() -> str: return sys.stdin.readline().rstrip()

n, m = map(int, input().split())

# [1, n] 중에서 중복 없이 m개를 고른 수열

def dfs(cur: list[int]):
    if len(cur) == m:
        print(*cur)
        return

    for digit in range(1, n + 1):
        if digit not in cur:
            dfs(cur + [digit])

dfs([])