# BOJ 15881 - Pen Pineapple Apple Pen
import sys
def input() -> str: return sys.stdin.readline().rstrip()

n = int(input())
S = input()
k = 'pPAp'

i = 0
cnt = 0
while i <= n - len(k):
    if S[i:i + len(k)] == k:
        cnt += 1
        i += len(k)
    else:
        i += 1

print(cnt)