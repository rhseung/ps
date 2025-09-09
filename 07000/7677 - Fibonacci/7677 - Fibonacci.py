# BOJ 7677 - Fibonacci
import sys
input = sys.stdin.readline

mod = 10000


def mul(a: int, b: int) -> int:
    return (a % mod) * (b % mod) % mod


def mul_2x2(mat1: list[list[int]], mat2: list[list[int]]) -> list[list[int]]:
    assert len(mat1) == 2 and len(mat1[0]) == 2
    assert len(mat2) == 2 and len(mat2[0]) == 2

    a = mat1[0][0]
    b = mat1[0][1]
    c = mat1[1][0]
    d = mat1[1][1]

    e = mat2[0][0]
    f = mat2[0][1]
    g = mat2[1][0]
    h = mat2[1][1]

    return [
        [(mul(a, e) + mul(b, g)) % mod, (mul(a, f) + mul(b, h)) % mod],
        [(mul(c, e) + mul(d, g)) % mod, (mul(c, f) + mul(d, h)) % mod],
    ]


def fast_pow(base: list[list[int]], exp: int) -> list[list[int]]:
    if exp == 0:
        return [[1, 0], [0, 1]]
    if exp == 1:
        return [[base[0][0] % mod, base[0][1] % mod], [base[1][0] % mod, base[1][1] % mod]]

    half = fast_pow(base, exp // 2)
    remain = base if exp % 2 == 1 else [[1, 0], [0, 1]]
    return mul_2x2(mul_2x2(half, half), remain)


def fibonacci(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    M_n = fast_pow([[1, 1], [1, 0]], n - 1)
    return M_n[0][0] % mod

def main():
    while True:
        n = int(input())
        if n == -1:
            break

        print(fibonacci(n))
    pass

if __name__ == "__main__":
    main()
