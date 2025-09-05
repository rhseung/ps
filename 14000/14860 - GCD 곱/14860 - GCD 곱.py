# BOJ 14860 - GCD 곱
import sys

input = sys.stdin.readline
MOD = 10 ** 9 + 7


# 0: 소수 후보, 1: 합성수
def sieve(limit: int):
    if limit < 2:
        return []
    
    is_comp = bytearray(limit + 1)
    is_comp[0] = is_comp[1] = 1

    for x in range(4, limit + 1, 2):
        is_comp[x] = 1

    r = int(limit ** 0.5)
    for i in range(3, r + 1, 2):
        if not is_comp[i]:
            step = i << 1
            start = i * i
            is_comp[start: limit + 1: step] = b"\x01" * (((limit - start) // step) + 1)

    primes = [2]
    primes.extend(i for i in range(3, limit + 1, 2) if not is_comp[i])
    return primes


def main():
    n, m = map(int, input().split())
    L = n if n < m else m

    primes = sieve(L)

    ans = 1
    for p in primes:
        # E_p = sum_{k>=1} floor(n / p^k) * floor(m / p^k)
        e = 0
        pk = p

        while pk <= L:
            e += (n // pk) * (m // pk)
            if e >= (1 << 63):
                e %= (MOD - 1)
            pk *= p

        e %= (MOD - 1)
        if e:
            ans = (ans * pow(p, e, MOD)) % MOD

    print(ans)


if __name__ == "__main__":
    main()
