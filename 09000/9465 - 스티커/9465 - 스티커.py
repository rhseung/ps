# BOJ 9465 - 스티커
import sys
input = sys.stdin.readline

def main():
    t = int(input())

    for _ in range(t):
        n = int(input())
        S = list(map(int, input().split())), list(map(int, input().split()))
        DP = [[0] * n for _ in range(3)]

        DP[0][0] = S[0][0]
        DP[1][0] = S[1][0]
        DP[2][0] = 0

        for w in range(1, n):
            DP[0][w] = max(DP[1][w - 1], DP[2][w - 1]) + S[0][w]
            DP[1][w] = max(DP[0][w - 1], DP[2][w - 1]) + S[1][w]
            DP[2][w] = max(DP[0][w - 1], DP[1][w - 1])

        print(max(DP[0][n - 1], DP[1][n - 1], DP[2][n - 1]))

if __name__ == "__main__":
    main()
