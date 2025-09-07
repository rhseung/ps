# BOJ 2293 - 동전 1
import sys
input = sys.stdin.readline

def main():
    n, k = map(int, input().split())
    V = [int(input()) for _ in range(n)]
    DP = [0] * (k + 1)
    DP[0] = 1

    for i in range(n):
        for x in range(V[i], k + 1):
            DP[x] += DP[x - V[i]]

    print(DP[k])

if __name__ == "__main__":
    main()
