# BOJ 1520 - 내리막 길
import sys

input = sys.stdin.readline


def main():
    h, w = map(int, input().split())
    M = [list(map(int, input().split())) for _ in range(h)]
    DP = [[0] * w for _ in range(h)]
    DP[0][0] = 1

    H: list[tuple[int, int, int]] = [(M[i][j], i, j) for j in range(w) for i in range(h)]
    H.sort(reverse=True)

    for v, i, j in H:
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if 0 <= i + di < len(M) and 0 <= j + dj < len(M[0]):
                if M[i + di][j + dj] > v:
                    DP[i][j] += DP[i + di][j + dj]

    print(DP[h - 1][w - 1])


if __name__ == "__main__":
    main()