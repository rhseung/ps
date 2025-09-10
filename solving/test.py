import time
from contextlib import contextmanager


@contextmanager
def timeit():
    start = time.time()
    yield
    end = time.time()
    print(f'{end - start}s')

def sieve(n: int):
    prime = [True] * (n + 1)
    prime[0] = False
    prime[1] = False

    i = 2
    while i * i <= n:
        if prime[i]:
            j = i * i
            while j <= n:
                prime[j] = False
                j += i
        i += 1

    return prime

def sieve_23(n: int):
    prime = [True] * (n + 1)
    prime[0] = False
    prime[1] = False

    # 2, 3을 제외한 소수는 전부 6n + 1, 6n + 5 꼴
    for i in range(n + 1):
        if i % 6 != 1 and i % 6 != 5:
            prime[i] = False

    i = 5
    while i * i <= n:
        if prime[i]:    # 6n + 5
            j = i * i
            while j <= n:
                prime[j] = False
                j += i

        ii = i + 2      # 6n + 1
        if prime[ii]:
            j = ii * ii
            while j <= n:
                prime[j] = False
                j += ii

        i += 6

    return prime

def to_prime_list(f, n: int):
    L = []
    S = f(n)
    for i in range(n + 1):
        if S[i]:
            L.append(i)

    return L

with timeit():
    print(to_prime_list(sieve, 100000000)[:10])

with timeit():
    print(to_prime_list(sieve, 100000000)[:10])
