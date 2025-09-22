# BOJ 13970 - Power towers
import math
import sys

input = sys.stdin.readline

MAX_V = 10 ** 6
is_composite = [False] * (MAX_V + 1)
primes = []
for i in range(2, MAX_V + 1):
    if not is_composite[i]:
        primes.append(i)
        step = i
        mul = i * i
        if mul <= MAX_V:
            for j in range(mul, MAX_V + 1, step):
                is_composite[j] = True


def factorize(n):
    res = []
    tmp = n
    for p in primes:
        if p * p > tmp: break
        if tmp % p == 0:
            k = 0
            while tmp % p == 0:
                tmp //= p
                k += 1
            res.append((p, k))
    if tmp > 1:
        res.append((tmp, 1))
    return res


def phi_of_prime_power(p, k):
    return (p ** k) - (p ** (k - 1))


def phi(n):
    ans = n
    for p, _ in factorize(n):
        ans -= ans // p
    return ans


def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


def modinv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        return None
    return x % m


def ge_power_tower(xs, i, L):
    if L <= 1:
        return True
    a = xs[i]
    if i == len(xs) - 1:
        return a >= L
    if a == 1:
        return 1 >= L

    T = math.ceil((math.log(L - 1 + 1e-12) / math.log(a)))
    return ge_power_tower(xs, i + 1, T)


def tower_with_cap(xs, i, cap):
    if cap <= 1:
        return cap
    a = xs[i]
    if i == len(xs) - 1:
        return a if a < cap else cap
    if a == 1:
        return 1
    T = math.ceil((math.log(cap - 1 + 1e-12) / math.log(a)))
    e = tower_with_cap(xs, i + 1, T)
    if e >= T:
        return cap
    return pow(a, e)


def tower_mod_with_flag(xs, i, mod):
    if i >= len(xs):
        return 1 % mod, False
    if mod == 1:
        return 0, True
    if i == len(xs) - 1:
        v = xs[i] % mod
        return v, (xs[i] >= mod)
    ph = phi(mod)
    sub_v, sub_big = tower_mod_with_flag(xs, i + 1, ph)
    exp = sub_v + (ph if sub_big else 0)
    val = pow(xs[i] % mod, exp, mod)
    big = ge_power_tower(xs, i, mod)
    return val, big


def solve_mod_pk(xs, p, k):
    if len(xs) == 1:
        return xs[0] % (p ** k)
    mod_pk = p ** k
    a = xs[0]
    r = 0
    tmp = a
    while tmp % p == 0:
        tmp //= p
        r += 1
    a1 = tmp

    if r > 0:
        need = (k + r - 1) // r
        if ge_power_tower(xs, 1, need):
            return 0
        E = tower_with_cap(xs, 1, need)
        pe = pow(p, r * E, mod_pk)
    else:
        pe = 1

    ph = phi_of_prime_power(p, k)
    e_mod, e_big = tower_mod_with_flag(xs, 1, ph)
    e_use = e_mod + (ph if e_big else 0)

    return (pe * pow(a1 % mod_pk, e_use, mod_pk)) % mod_pk


def crt_pair(a1, m1, a2, m2):
    inv = modinv(m1 % m2, m2)
    t = ((a2 - a1) % m2) * inv % m2
    return a1 + m1 * t, m1 * m2


t, m = map(int, input().split())
fac_M = factorize(m)
pk_list = [(p, k, p ** k) for (p, k) in fac_M]

for _ in range(t):
    n, *xs = map(int, input().split())
    if m == 1:
        print(0)
        continue

    cur_a, cur_m = 0, 1
    for p, k, mod_pk in pk_list:
        ai = solve_mod_pk(xs, p, k)
        if cur_m == 1:
            cur_a, cur_m = ai % mod_pk, mod_pk
        else:
            cur_a, cur_m = crt_pair(cur_a, cur_m, ai % mod_pk, mod_pk)

    print(cur_a % m)
