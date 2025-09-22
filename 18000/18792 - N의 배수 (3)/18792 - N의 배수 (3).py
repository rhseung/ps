# BOJ 18792 - N의 배수 (3)
import sys

input = sys.stdin.readline


def modpow(base: int, exp: int, m: int) -> int:
    return pow(base, exp, m)


def modinv(d: int, p: int) -> int:
    return pow(d, p - 2, p)


def find(p: int, T_c: list[bool], d: int, u: int, v: int) -> int:
    d_inv = modinv(d, p)
    left = (u * d_inv) % p
    right = p + ((v * d_inv) % p)

    while left < right:
        m = (left + right) // 2
        i = ((m % p) * d) % p

        if T_c[i]:
            left = m + 1
        else:
            right = m

    return (right % p) * d % p


def prime_egz(p: int, N: list[int]) -> list[bool]:
    K = list(range(2 * p - 1))
    K.sort(key=lambda x: N[x] % p)

    R = [False] * (2 * p - 1)

    for i in range(p - 1):
        if (N[K[1 + i]] % p) == (N[K[p + i]] % p):
            for j in range(i + 1, i + p + 1):
                R[K[j]] = True
            return R

    s = 0
    for i in range(p):
        s = (s + N[K[i]]) % p

    T_c = [False] * p
    T_indices = [None] * p
    T_c[s] = True

    for i in range(1, p):
        if T_c[0]:
            break
        diff = (N[K[p + i - 1]] - N[K[i]]) % p
        t = find(p, T_c, diff, s, 0)
        T_c[t] = True
        T_indices[t] = i

    for i in range(p):
        R[K[i]] = True

    c = 0
    while s != c:
        idx = T_indices[c]
        R[K[p + idx - 1]] = True
        R[K[idx]] = False
        diff = (N[K[p + idx - 1]] - N[K[idx]]) % p
        c = (c - diff) % p

    return R


def composite_egz(p: int, q: int, N: list[int]) -> list[bool]:
    S = list(range(p - 1))
    T_group: list[list[int] | None] = [None] * (2 * q - 1)

    for i in range(2 * q - 1):
        start = (i + 1) * p - 1
        end = (i + 2) * p - 1
        for val in range(start, end):
            S.append(val)

        N_sub = [N[idx] for idx in S]
        R_p = egz(p, N_sub)

        selected = []
        not_selected = []
        for j in range(2 * p - 1):
            if R_p[j]:
                selected.append(S[j])
            else:
                not_selected.append(S[j])

        T_group[i] = selected
        S = not_selected

    R = [False] * (2 * p * q - 1)
    S_div_p = []

    for i in range(2 * q - 1):
        group = T_group[i]
        total = 0
        for idx in group:
            total += N[idx]
        S_div_p.append(total // p)

    R_q = egz(q, S_div_p)

    for i in range(2 * q - 1):
        if R_q[i]:
            for idx in T_group[i]:
                R[idx] = True

    return R


def egz(n: int, N: list[int]) -> list[bool]:
    if n == 1:
        return [True]

    for i in range(2, n):
        if n % i == 0:
            return composite_egz(i, n // i, N)

    return prime_egz(n, N)


n = int(input())
N = list(map(int, input().split()))
R = egz(n, N)

for i in range(2 * n - 1):
    if R[i]:
        print(N[i], end=' ')
