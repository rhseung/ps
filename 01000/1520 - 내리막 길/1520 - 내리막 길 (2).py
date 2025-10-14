# BOJ 1520 - 내리막 길
import sys
sys.setrecursionlimit(10**6)

input = sys.stdin.readline

def dfs(now: tuple[int, int], M: list[list[int]], DP: list[list[int]]):
    r, c = now

    if DP[r][c] != -1:
        return DP[r][c]
    else:
        DP[r][c] = 0

    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if 0 <= r + dr < len(M) and 0 <= c + dc < len(M[0]):
            if M[r + dr][c + dc] > M[r][c]:
                DP[r][c] += dfs((r + dr, c + dc), M, DP)

    return DP[r][c]

def main():
    h, w = map(int, input().split())
    M = [list(map(int, input().split())) for _ in range(h)]
    DP = [[-1] * w for _ in range(h)]
    DP[0][0] = 1

    print(dfs((h - 1, w - 1), M, DP))

if __name__ == "__main__":
    main()
