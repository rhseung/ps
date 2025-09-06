# BOJ 11691 - LCM(i, j)

import sys
input = sys.stdin.readline

MOD = 1_000_000_007
INV2 = 500_000_004  # inverse of 2 mod MOD

def sieve_g(n: int):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    h = [1] * (n + 1)

    for p in range(2, n+1):
        if is_prime[p]:
            step = p
            for k in range(p * p, n + 1, step):
                is_prime[k] = False
            factor = (1 - p) % MOD
            for m in range(p, n+1, p):
                h[m] = (h[m] * factor) % MOD

    g = [0] * (n + 1)
    for m in range(1, n+1):
        g[m] = (m % MOD) * h[m] % MOD
    return g


def T2(x: int) -> int:
    t = x % MOD
    t = (t * ((x + 1) % MOD)) % MOD
    t = (t * INV2) % MOD
    return (t * t) % MOD

def main():
    n = int(input().strip())

    g = sieve_g(n)
    pref = [0] * (n + 1)
    acc = 0
    for i in range(1, n + 1):
        acc = (acc + g[i]) % MOD
        pref[i] = acc

    # S_all = sum_{l=1..n} g(l) * T(floor(n/l))^2 where T(x) = x(x+1)/2
    S_all = 0
    l = 1
    while l <= n:
        q = n // l
        r = n // q
        sum_g = (pref[r] - pref[l-1]) % MOD
        S_all = (S_all + sum_g * T2(q)) % MOD
        l = r + 1

    diag = (n % MOD) * ((n + 1) % MOD) % MOD
    diag = (diag * INV2) % MOD
    ans = (S_all - diag) % MOD
    ans = (ans * INV2) % MOD
    print(ans)

if __name__ == "__main__":
    main()
