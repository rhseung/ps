# BOJ 14225 - 부분수열의 합
import sys
def input() -> str: return sys.stdin.readline()

n = int(input())
S = list(map(int, input().split()))

min_v = min(S)
sum_v = sum(S)

A = [False] * (sum_v + 1)

def dfs(i: int, cur: int):
    if i >= n:
        return

    A[cur + S[i]] = True

    dfs(i + 1, cur)
    dfs(i + 1, cur + S[i])


dfs(0, 0)

for i in range(1, sum_v + 1):
    if not A[i]:
        print(i)
        exit()

print(sum_v + 1)