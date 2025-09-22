# BOJ 18792 - N의 배수 (3)
import sys

input = sys.stdin.readline


def modpow(base: int, exp: int, m: int) -> int:
    return pow(base, exp, m)


def modinv(d: int, p: int) -> int:
    return pow(d, p - 2, p)


def find(p: int, t_check: list[bool], d: int, u: int, v: int) -> int:
    d_inv = modinv(d, p)
    left = (u * d_inv) % p
    right = p + ((v * d_inv) % p)

    while left < right:
        m = (left + right) // 2
        if t_check[((m % p) * d) % p]:
            left = m + 1
        else:
            right = m

    return (right % p) * d % p


def prime_egz(p: int, nums: list[int]) -> list[bool]:
    k = list(range(2 * p - 1))
    k.sort(key=lambda x: nums[x] % p)

    ret = [False] * (2 * p - 1)

    for i in range(p - 1):
        if (nums[k[1 + i]] % p) == (nums[k[p + i]] % p):
            for j in range(i + 1, i + p + 1):
                ret[k[j]] = True
            return ret

    s = 0
    for i in range(p):
        s = (s + nums[k[i]]) % p

    t_check = [False] * p
    t_idxes = [None] * p
    t_check[s] = True

    for i in range(1, p):
        if t_check[0]:
            break
        diff = (nums[k[p + i - 1]] - nums[k[i]]) % p
        t = find(p, t_check, diff, s, 0)
        t_check[t] = True
        t_idxes[t] = i

    for i in range(p):
        ret[k[i]] = True

    c = 0
    while s != c:
        idx = t_idxes[c]
        ret[k[p + idx - 1]] = True
        ret[k[idx]] = False
        diff = (nums[k[p + idx - 1]] - nums[k[idx]]) % p
        c = (c - diff) % p

    return ret


def composite_egz(p: int, q: int, nums: list[int]) -> list[bool]:
    s = list(range(p - 1))
    t_groups: list[list[int] | None] = [None] * (2 * q - 1)

    for i in range(2 * q - 1):
        start = (i + 1) * p - 1
        end = (i + 2) * p - 1
        for val in range(start, end):
            s.append(val)

        nums_sub = [nums[idx] for idx in s]
        ret_p = egz(p, nums_sub)

        selected = []
        not_selected = []
        for j in range(2 * p - 1):
            if ret_p[j]:
                selected.append(s[j])
            else:
                not_selected.append(s[j])

        t_groups[i] = selected
        s = not_selected

    ret = [False] * (2 * p * q - 1)
    sum_div_p = []

    for i in range(2 * q - 1):
        group = t_groups[i]
        total = 0
        for idx in group:
            total += nums[idx]
        sum_div_p.append(total // p)

    ret_q = egz(q, sum_div_p)

    for i in range(2 * q - 1):
        if ret_q[i]:
            for idx in t_groups[i]:
                ret[idx] = True

    return ret


def egz(n: int, nums: list[int]) -> list[bool]:
    if n == 1:
        return [True]

    for i in range(2, n):
        if n % i == 0:
            return composite_egz(i, n // i, nums)

    return prime_egz(n, nums)


n = int(input())
nums = list(map(int, input().split()))
ret = egz(n, nums)

for i in range(2 * n - 1):
    if ret[i]:
        print(nums[i], end=' ')
