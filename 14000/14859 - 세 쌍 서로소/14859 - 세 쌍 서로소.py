# BOJ 14859 - 세 쌍 서로소
import sys
input = sys.stdin.readline

n = int(input())
A = list(map(int, input().split()))

if n < 3:
    print(0)
    exit(0)

MAX_A = 10 ** 6
freq = [0] * (MAX_A + 1)
for x in A:
    if x <= MAX_A:
        freq[x] += 1

cnt = [0] * (MAX_A + 1)
for d in range(1, MAX_A + 1):
    s = 0
    for m in range(d, MAX_A + 1, d):
        s += freq[m]
    cnt[d] = s

mu = [0] * (MAX_A + 1)
mu[1] = 1
least_prime = [0] * (MAX_A + 1)
primes = []

for i in range(2, MAX_A + 1):
    if least_prime[i] == 0:
        least_prime[i] = i
        primes.append(i)
        mu[i] = -1

    for p in primes:
        v = i * p
        if v > MAX_A:
            break
        least_prime[v] = p
        if i % p == 0:
            mu[v] = 0
            break
        else:
            mu[v] = -mu[i]

def comb3(c: int) -> int:
    if c < 3:
        return 0
    return c * (c - 1) * (c - 2) // 6

ans = 0
for d in range(1, MAX_A + 1):
    c = cnt[d]
    if c >= 3 and mu[d] != 0:
        ans += mu[d] * comb3(c)

print(ans)
