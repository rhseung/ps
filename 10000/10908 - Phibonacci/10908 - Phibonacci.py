# BOJ 10908 - Phibonacci
import sys

input = sys.stdin.readline

mod = 1000000007

def mul_mod(a: int, b: int, MOD: int) -> int:
    return (a % MOD) * (b % MOD) % MOD


def mul_2x2_mod(mat1: list[list[int]], mat2: list[list[int]], MOD: int) -> list[list[int]]:
    assert len(mat1) == 2 and len(mat1[0]) == 2
    assert len(mat2) == 2 and len(mat2[0]) == 2

    a = mat1[0][0]; b = mat1[0][1]
    c = mat1[1][0]; d = mat1[1][1]

    e = mat2[0][0]; f = mat2[0][1]
    g = mat2[1][0]; h = mat2[1][1]

    return [
        [(mul_mod(a, e, MOD) + mul_mod(b, g, MOD)) % MOD, (mul_mod(a, f, MOD) + mul_mod(b, h, MOD)) % MOD],
        [(mul_mod(c, e, MOD) + mul_mod(d, g, MOD)) % MOD, (mul_mod(c, f, MOD) + mul_mod(d, h, MOD)) % MOD],
    ]


def fast_pow_mod(base: list[list[int]], exp: int, MOD: int) -> list[list[int]]:
    if exp == 0:
        return [[1, 0], [0, 1]]
    if exp == 1:
        return [[base[0][0] % MOD, base[0][1] % MOD], [base[1][0] % MOD, base[1][1] % MOD]]

    half = fast_pow_mod(base, exp // 2, MOD)
    remain = base if exp % 2 == 1 else [[1, 0], [0, 1]]
    return mul_2x2_mod(mul_2x2_mod(half, half, MOD), remain, MOD)


def fibonacci_mod(n: int, MOD: int) -> tuple[int, int]:
    if n == 0:
        return 0, 1
    if n == 1:
        return 1, 0
    M_n = fast_pow_mod([[1, 1], [1, 0]], n - 1, MOD)
    return M_n[0][0] % MOD, M_n[1][0] % MOD


def main():
    n, k = map(int, input().split())

    mod_2 = mod * mod
    f_nk, f_nk_1 = fibonacci_mod(n * k, mod_2)
    f_k, f_k_1 = fibonacci_mod(k, mod_2)

    if f_k % mod == 0:
        f_nk //= mod
        f_k //= mod

    a = f_nk * pow(f_k, -1, mod) % mod
    b = (f_nk_1 - a * f_k_1) % mod

    print(a, b)

    pass


if __name__ == "__main__":
    main()