# BOJ 22940 - 선형 연립 방정식
import sys
from fractions import Fraction

def input() -> str: return sys.stdin.readline()

n = int(input())
M = [list(map(lambda x: Fraction(x), input().split())) for _ in range(n)]

for col in range(n):
    pivot = col
    for r in range(col, n):
        if M[r][col] != 0:
            pivot = r
            break

    if pivot != col:
        M[col], M[pivot] = M[pivot], M[col]

    piv = M[col][col]
    if piv != 1:
        for c in range(col, n + 1):
            M[col][c] /= piv

    for r in range(n):
        if r == col:
            continue

        factor = M[r][col]
        if factor == 0:
            continue
        for c in range(col, n + 1):
            M[r][c] -= factor * M[col][c]

ans = [M[i][n] for i in range(n)]

for x in ans:
    if x.denominator != 1:
        rounded = int(x)
        if Fraction(rounded) != x:
            rounded = x.numerator // x.denominator
        print(rounded, end=" ")
    else:
        print(x.numerator, end=" ")