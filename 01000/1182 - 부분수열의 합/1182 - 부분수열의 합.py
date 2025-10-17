# BOJ 1182 - 부분수열의 합
import sys
def input() -> str: return sys.stdin.readline()

n, k = map(int, input().split())
A = list(map(int, input().split()))

ans = 0

def dfs(i: int, cur: int):
    if i >= n:
        return

    if cur + A[i] == k:
        global ans
        ans += 1

    dfs(i + 1, cur + A[i])
    dfs(i + 1, cur)

dfs(0, 0)
print(ans)
