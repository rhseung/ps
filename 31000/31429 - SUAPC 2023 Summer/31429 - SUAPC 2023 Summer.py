# BOJ 31429 - SUAPC 2023 Summer
import sys
def input() -> str: return sys.stdin.readline().rstrip()

data = [
    [12, 1600],
    [11, 894],
    [11, 1327],
    [10, 1311],
    [9, 1004],
    [9, 1178],
    [9, 1357],
    [8, 837],
    [7, 1055],
    [6, 556],
    [6, 773]
]

n = int(input())
print(*data[n - 1])
