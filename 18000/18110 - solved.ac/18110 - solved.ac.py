# BOJ 18110 - solved.ac
import sys
from math import floor


def input() -> str: return sys.stdin.readline().rstrip()

def round_to_int(x: float) -> int:
    return int(floor(x + 0.5))

n = int(input())
S = [int(input()) for _ in range(n)]

part = round_to_int(n * 0.15)
S.sort()

l = n - 2 * part
if l == 0:
    print(0)
else:
    print(round_to_int(sum(S[part:n - part]) / l))

# print(f"{part=}, {S=}, {l=}, {S[part:n - part]=}, {(sum(S[part:n - part]) / l)=}")