# BOJ 2294 - 동전 2
import sys
input = sys.stdin.readline
inf = float('inf')

def main():
    n, k = map(int, input().split())
    V = [int(input()) for _ in range(n)]
    DP = [inf] * (k + 1)
    DP[0] = 0

    for x in range(0, k + 1):
        DP[x] = min((DP[x - V[i]] + 1 for i in range(n) if x >= V[i]), default=DP[x])

    # print(DP)
    print(-1 if DP[k] == inf else DP[k])

if __name__ == "__main__":
    main()
