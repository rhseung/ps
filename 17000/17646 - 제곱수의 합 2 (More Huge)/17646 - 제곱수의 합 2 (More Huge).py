# BOJ 17646 - 제곱수의 합 2 (More Huge)
from collections import Counter
from math import floor
from math import gcd
from math import isqrt
from math import sqrt
from random import randint, randrange
from sys import stdin

input = stdin.readline


def is_square(n: int) -> bool:
    return n == isqrt(n) ** 2


def miller_rabin(n: int, a: int) -> bool:
    s = 0
    tmp = n - 1
    while tmp % 2 == 0:
        tmp //= 2
        s += 1
    d = tmp

    p = pow(a, d, n)
    if p == 1 or p == n - 1:
        return True

    x = pow(a, d, n)
    for r in range(s):
        if x == n - 1:
            return True
        x = pow(x, 2, n)

    return False


def is_prime(n: int) -> bool:
    if n == 1:
        return False
    elif n == 2:
        return True
    elif n % 2 == 0:
        return False

    alist = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
    for a in alist:
        if n == a:
            return True

        is_probable_prime = miller_rabin(n, a)
        if not is_probable_prime:
            return False

    return True


def pollard_rho(n: int, i: int) -> int:
    if is_prime(n):
        return n
    elif n % 2 == 0:
        return 2

    g = lambda x_: (x_ ** 2 + i) % n
    x = randint(1, floor(sqrt(n - 1))) ** 2 + 1
    y = x
    d = 1

    while d == 1:
        x = g(x)
        y = g(g(y))
        d = gcd(abs(x - y), n)

    if d == n:
        return pollard_rho(n, i + 2)
    elif is_prime(d):
        return d
    else:
        return pollard_rho(d, 1)


def get_factors(n):
    factors = []

    while n > 1:
        factor = pollard_rho(n, 1)
        factors.append(factor)
        n //= factor

    factors.sort()
    return factors


def get_counts(n: int) -> int:
    factors = Counter(get_factors(n))

    if is_square(n):
        return 1

    flag = True
    for key, value in factors.items():
        if key % 4 == 3 and value % 2 == 1:
            flag = False

    if flag:
        return 2

    tmp = n
    while tmp % 4 == 0:
        tmp //= 4

    if tmp % 8 != 7:
        return 3

    return 4

# https://en.wikipedia.org/wiki/Tonelli%E2%80%93Shanks_algorithm
# x^2 = -1 (mod p) 를 구할 수 있는 알고리즘
def tonelli(p: int) -> int:
    n = p - 1
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1

    z = randrange(2, p - 1)
    while pow(z, (p - 1) // 2, p) == 1:
        z = randrange(2, p - 1)

    m = s
    c = pow(z, q, p)
    t = pow(n, q, p)
    r = pow(n, (q + 1) // 2, p)

    if t == 0:
        return 0

    while t != 1 and t != 0:
        tt = t
        i = 0
        while t % p != 1:
            t = (t * t) % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m = i
        c = (b * b) % p
        t = (tt * c) % p
        r = (r * b) % p

    return r

# https://en.wikipedia.org/wiki/Cornacchia%27s_algorithm
# x^2 + y^2 = p (mod p) (prime p ≡ 1 mod 4) 를 구할 수 있는 알고리즘
# p ≡ 3 (mod 4) 인 경우 None 반환
def cornacchia(p: int) -> tuple[int, int] | None:
    if p % 4 == 3:
        return None
    if p == 2:
        return 1, 1  # 1^2 + 1^2 = 2

    r = tonelli(p)  # r^2 ≡ -1 (mod p)

    # 유클리드 (p, r), r^2 ≤ p 일 때까지
    a, b = p, r
    while b * b > p:
        a, b = b, a % b

    x2 = b * b
    y2 = p - x2
    return b, int(y2 ** 0.5)

# 브라흐마굽타-피보나치 항등식
# (ac+bd)^2 + (ad-bc)^2 = (a^2 + b^2)(c^2 + d^2)
def brahmagupta(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    x1, y1 = a
    x2, y2 = b
    return abs(x1 * x2 + y1 * y2), abs(x1 * y2 - y1 * x2)

# n = mul^2 * core * 2^e 꼴로 분해하는 함수 (단, 2의 처리는 build_2에서 별도 합성)
def separate(n: int) -> tuple[int, int, dict[int, int]]:
    fd = Counter(get_factors(n))
    mul = 1
    core = 1
    for p, e in fd.items():
        if p == 2:
            continue
        mul *= p ** (e // 2)
        if e % 2 == 1:
            core *= p

    return mul, core, fd

def build_1(n: int) -> tuple[int]:
    return isqrt(n),

def build_2(n: int) -> tuple[int, int]:
    # n = mul^2 * core * 2^e (core: primes ≡ 1 (mod 4) with odd exponent)
    mul, core, fd = separate(n)

    x, y = 1, 0
    for p, e in fd.items():
        if (e % 2 == 1) and (p % 4 == 1):
            sol = cornacchia(p)  # a^2 + b^2 = p
            if sol is not None:
                x, y = brahmagupta((x, y), sol)

    # 2 = 1^2 + 1^2
    twos = fd.get(2, 0)
    if twos % 2 == 1:
        x, y = brahmagupta((x, y), (1, 1))

    scale = mul * (1 << (twos // 2))
    return scale * x, scale * y

def build_3(n: int) -> tuple[int, int, int]:
    # core - t^2가 2제곱수 합이 되는 순간을 찾기

    mul, core, fd = separate(n)

    twos = fd.get(2, 0)
    scale = mul * (1 << (twos // 2))
    Tcore = core << (twos % 2)
    t = 0
    while t * t <= Tcore:
        if get_counts(Tcore - t * t) == 2:
            a, b = build_2(Tcore - t * t)
            return scale * a, scale * b, scale * t
        t += 1

    # naive
    for i in range(isqrt(n), 0, -1):
        m = n - i * i
        for j in range(isqrt(m), 0, -1):
            if is_square(m - j * j):
                return i, j, isqrt(m - j * j)

    return None


def build_4(n: int) -> tuple[int, int, int, int]:
    # n - 1 = mul * core * (t^2)

    ct = 0
    m = n
    while m % 4 == 0:
        m //= 4
        ct += 1

    a, b, c = build_3(m - 1)
    scale = 1 << ct

    return a * scale, b * scale, c * scale, scale

def main():
    n = int(input())
    cnt = get_counts(n)

    print(cnt)

    match cnt:
        case 1:
            a, = build_1(n)
            print(a)
        case 2:
            a, b = build_2(n)
            print(a, b)
        case 3:
            a, b, c = build_3(n)
            print(a, b, c)
        case 4:
            a, b, c, d = build_4(n)
            print(a, b, c, d)


if __name__ == "__main__":
    main()
