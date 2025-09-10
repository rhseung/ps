# BOJ 8291 - Coprime Numbers
import sys

input = sys.stdin.readline

MAX = 3_000_001
A = [0] * MAX
B = [0] * MAX
C = [0] * MAX
D = [0] * MAX

def main():
    n = int(input())

    # A[i] = i의 개수
    for v in map(int, input().split()):
        A[v] += 1

    # B[i] = i의 배수의 개수
    for i in range(1, MAX):
        for j in range(i, MAX, i):
            B[i] += A[j]

    # C[i] = gcd가 i의 배수인 쌍의 개수
    for i in range(1, MAX):
        C[i] = B[i] * (B[i] - 1) // 2

    # D[i] = gcd가 i인 쌍의 개수
    for i in range(MAX - 1, 0, -1):
        D[i] = C[i]
        for j in range(2 * i, MAX, i):
            D[i] -= D[j]

    print(D[1])

if __name__ == "__main__":
    main()
