# BOJ 5647 - 연속 합
import sys
from math import floor, sqrt, gcd
from random import randint

input = sys.stdin.readline


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

    g = lambda x: (x ** 2 + i) % n
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


def count_divisors_of_2q2(q: int) -> int:
    facs = get_factors(q)
    exp = {}
    for f in facs:
        exp[f] = exp.get(f, 0) + 1
    ans = 2
    for p, e in exp.items():
        if p == 2:
            continue
        ans *= (2 * e + 1)
    return ans


while True:
    q = int(input())
    if q == 0:
        break

    print(count_divisors_of_2q2(q))
