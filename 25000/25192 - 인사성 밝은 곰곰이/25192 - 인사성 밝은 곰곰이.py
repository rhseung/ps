# BOJ 25192 - 인사성 밝은 곰곰이
import sys
def input() -> str: return sys.stdin.readline().rstrip()

n = int(input())
cnt = 0
uniq = set()
for _ in range(n):
    s = input()
    if s != 'ENTER':
        uniq.add(s)
    else:
        cnt += len(uniq)
        uniq.clear()
cnt += len(uniq)

print(cnt)