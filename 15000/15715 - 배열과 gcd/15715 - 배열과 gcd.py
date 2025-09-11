# BOJ 15715 - 배열과 gcd
import sys
input = sys.stdin.readline

MOD = 1_000_000_007
MAX_P = 31623
is_prime = [True] * (MAX_P + 1)
is_prime[0] = is_prime[1] = False
primes = []

for i in range(2, MAX_P + 1):
    if is_prime[i]:
        primes.append(i)
        step = i
        start = i * i
        if start <= MAX_P:
            for j in range(start, MAX_P + 1, step):
                is_prime[j] = False

D: dict[int, tuple[int, ...]] = {}

def distinct_prime_factors(n: int) -> tuple[int, ...]:
    if n in D:
        return D[n]

    x = n
    res = []
    for p in primes:
        if p*p > x:
            break
        if x % p == 0:
            res.append(p)
            while x % p == 0:
                x //= p
    if x > 1:
        res.append(x)
    tup = tuple(res)
    D[n] = tup
    return tup

def count_coprime_upto(M: int, A: int) -> int:
    if M <= 0:
        return 0
    if A == 1:
        return M
    
    pf = distinct_prime_factors(A)
    k = len(pf)
    total = M
    
    for mask in range(1, 1 << k):
        prod = 1
        bits = 0
        mm = mask
        idx = 0
        while mm:
            if mm & 1:
                prod *= pf[idx]
                bits += 1
                if prod > M:
                    break
            idx += 1
            mm >>= 1
        if prod <= M:
            cnt = M // prod
            if bits % 2 == 1:
                total -= cnt
            else:
                total += cnt
    
    return total

n, num = map(int, input().split())
C = list(map(int, input().split()))

if len(C) != n:
    C += list(map(int, sys.stdin.read().split()))
    C = C[:n]

if C[0] > num:
    print(0)
    exit()

for i in range(1, n):
    if C[i-1] % C[i] != 0:
        print(0)
        exit()

ans = 1
for i in range(1, n):
    a = C[i-1]
    b = C[i]
    A = a // b
    M = num // b
    ways = count_coprime_upto(M, A)
    if ways == 0:
        print(0)
        exit()
    
    ans = (ans * (ways % MOD)) % MOD

print(ans % MOD)
