# BOJ 1157 - 단어 공부
import sys
from collections import Counter


def input() -> str: return sys.stdin.readline().rstrip()

F = Counter(input().lower())
M = F.most_common(2)

# print(M)
print('?' if len(M) == 2 and M[0][1] == M[1][1] else M[0][0].upper())
