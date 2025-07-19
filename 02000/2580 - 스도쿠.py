__problem__ = 'https://boj.kr/2580', '스도쿠'

import sys

input = sys.stdin.readline

M = [[] for _ in range(9)]
zeros = []

for i in range(9):
    M[i] = list(map(int, input().split()))
    for j in range(9):
        if M[i][j] == 0:
            zeros.append((i, j))

def square_check(i: int, j: int, val: int) -> bool:
    for i_ in range(3):
        for j_ in range(3):
            a, b = 3*(i // 3) + i_, 3*(j // 3) + j_
            if (i, j) != (a, b) and M[a][b] == val:
                return False
    return True

def line_check(i: int, j: int, val: int) -> bool:
    for a in range(9):
        if i != a and M[a][j] == val:
            return False
        if j != a and M[i][a] == val:
            return False
    return True

def dfs(idx):
    if idx >= len(zeros):
        for i in range(9):
            print(*M[i], sep=' ')
        exit()

    i, j = zeros[idx]
    for v in range(1, 10):
        if square_check(i, j, v) and line_check(i, j, v):
            M[i][j] = v
            dfs(idx + 1)
            M[i][j] = 0

dfs(0)
