# BOJ 12865 - 평범한 배낭
import sys
input = sys.stdin.readline

def main():
    n, k = map(int, input().split())
    W = [0] * (n + 1)
    V = [0] * (n + 1)
    DP = [[0] * (k + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        W[i], V[i] = map(int, input().split())

    for i in range(1, n + 1):
        for w in range(1, k + 1):
            if w >= W[i]:
                DP[i][w] = max(DP[i - 1][w], DP[i - 1][w - W[i]] + V[i])
            else:
                DP[i][w] = DP[i - 1][w]

    print(DP[n][k])

if __name__ == "__main__":
    main()
