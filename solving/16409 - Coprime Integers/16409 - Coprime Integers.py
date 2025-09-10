# BOJ 16409 - Coprime Integers
import sys

input = sys.stdin.readline

MAX = 10**7 + 1
C = [0] * MAX
D = [0] * MAX

def main():
    a, b, c, d = map(int, input().split())
    a -= 1
    c -= 1

    # C[i] = gcd가 i의 배수인 쌍의 개수
    for i in range(1, MAX):
        C[i] = (b // i - a // i) * (d // i - c // i)

    # D[i] = gcd가 i인 쌍의 개수
    for i in range(MAX - 1, 0, -1):
        D[i] = C[i]
        for j in range(2 * i, MAX, i):
            D[i] -= D[j]

    print(D[1])

if __name__ == "__main__":
    main()
