# BOJ 1018 - 체스판 다시 칠하기
import sys
def input() -> str: return sys.stdin.readline().rstrip()

# W로 시작하거나 B로 시작하는 두 가지 경우로 구해서 에러 최소 구하면 됨

n, m = map(int, input().split())
board = [list(input()) for _ in range(n)]

min_error = sys.maxsize
for offset_i in range(n - 7):
    for offset_j in range(m - 7):
        error_W = 0
        error_B = 0
        for i in range(offset_i, offset_i + 8):
            for j in range(offset_j, offset_j + 8):
                if (i + j) % 2 == 0:
                    error_W += int(board[i][j] != 'W')
                    error_B += int(board[i][j] != 'B')
                else:
                    error_W += int(board[i][j] != 'B')
                    error_B += int(board[i][j] != 'W')

        min_error = min(min_error, error_W, error_B)

print(min_error)