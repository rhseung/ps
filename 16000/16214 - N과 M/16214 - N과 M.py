# BOJ 16214 - N과 M
import sys
from math import ceil, log

input = sys.stdin.readline


def factorize(n: int):
    res = []
    x = n
    d = 2
    while d * d <= x:
        if x % d == 0:
            k = 0
            while x % d == 0:
                x //= d
                k += 1
            res.append((d, k))
        d = 3 if d == 2 else d + 2
    if x > 1:
        res.append((x, 1))
    return res


def phi_prime_power(p: int, k: int) -> int:
    return (p ** k) - (p ** (k - 1))


def phi(n: int) -> int:
    ans = n
    for p, _ in factorize(n):
        ans -= ans // p
    return ans


def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


def inv_mod(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        return None
    return x % m


EPS = 1e-12


def ge_tower_constN(N: int, L: int) -> bool:
    if L <= 1:
        return True
    if N == 1:
        return 1 >= L

    T = ceil((log(max(L - 1, 1)) + 0.0) / log(N))
    return ge_tower_constN(N, T)


def tower_with_cap_constN(N: int, cap: int) -> int:
    if cap <= 1:
        return cap
    if N == 1:
        return 1
    T = ceil((log(max(cap - 1, 1)) + 0.0) / log(N))
    e = tower_with_cap_constN(N, T)
    if e >= T:
        return cap

    return N ** e


def tower_limit_mod_constN(N: int, m: int) -> int:
    if m == 1:
        return 0
    ph = phi(m)
    e = tower_limit_mod_constN(N, ph)
    return pow(N % m, e + ph, m)


def solve_mod_pk_constN(N: int, p: int, k: int) -> int:
    mod_pk = p ** k
    r = 0
    tmp = N
    while tmp % p == 0 and tmp > 0:
        tmp //= p
        r += 1
    a = tmp

    if r > 0:
        need = (k + r - 1) // r
        if ge_tower_constN(N, need):
            return 0

        E_small = tower_with_cap_constN(N, need)
        pe = pow(p, r * E_small, mod_pk)
    else:
        pe = 1

    ph = phi_prime_power(p, k)
    e_mod = tower_limit_mod_constN(N, ph)
    exp = e_mod + ph
    return (pe * pow(a % mod_pk, exp, mod_pk)) % mod_pk


def crt_pair(a1, m1, a2, m2):
    inv = inv_mod(m1 % m2, m2)
    t = ((a2 - a1) % m2) * inv % m2
    return a1 + m1 * t, m1 * m2


t = int(input().strip())
for _ in range(t):
    n, m = map(int, input().split())
    if m == 1:
        print(0)
        continue
    if n == 1:
        print(1 % m)
        continue

    fac = factorize(m)
    cur_a, cur_m = 0, 1
    for p, k in fac:
        ai = solve_mod_pk_constN(n, p, k)
        if cur_m == 1:
            cur_a, cur_m = ai % (p ** k), (p ** k)
        else:
            cur_a, cur_m = crt_pair(cur_a, cur_m, ai % (p ** k), (p ** k))

    print(cur_a % m)
