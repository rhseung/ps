# BOJ 2294 - 동전 2
import sys
input = sys.stdin.readline

def main():
    n, k = map(int, input().split())
    V = [int(input()) for _ in range(n)]
    DP = [0] * (k + 1)

    for x in range(0, k + 1):
        DP[x] = min(DP[k - V[i]] + 1 for i in range(n) if k >= V[i])

    print(DP)
    print(DP[k])

if __name__ == "__main__":
    main()
