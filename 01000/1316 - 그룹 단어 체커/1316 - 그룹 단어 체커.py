# BOJ 1316 - 그룹 단어 체커
import sys
def input() -> str: return sys.stdin.readline().rstrip()

n = int(input())
cnt = 0
for _ in range(n):
    s = input()

    visited = []
    for i in range(len(s)):
        if s[i] not in visited:
            visited.append(s[i])
        elif visited[-1] != s[i]:
            break
    else:
        cnt += 1

print(cnt)