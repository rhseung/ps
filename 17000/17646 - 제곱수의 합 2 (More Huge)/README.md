# 17646. [제곱수의 합 2 (More Huge)](https://www.acmicpc.net/problem/17646)

| 티어 | 시간 제한 | 메모리 제한 | 제출 | 정답 | 맞힌 사람 | 정답 비율 |
|---|---|---|---:|---:|---:|---:|
| <img src="https://static.solved.ac/tier_small/27.svg" width="20px" /> | 0.5 초 (추가 시간 없음) | 512 MB | 2420 | 383 | 192 | 10.891% |

---

## 문제

라그랑주는 1770년에 모든 자연수는 넷 혹은 그 이하의 제곱수의 합으로 표현할 수 있다고 증명하였다. 어떤 자연수는 복수의 방법으로 표현된다. 예를 들면, 26은 $5^{2}$
과 $1^{2}$
의 합이다; 또한 $4^{2}$ + $3^{2}$ + $1^{2}$
으로 표현할 수도 있다. 역사적으로 암산의 명수들에게 공통적으로 주어지는 문제가 바로 자연수를 넷 혹은 그 이하의 제곱수 합으로 나타내라는 것이었다. 1900년대 초반에 한 암산가가 15663 = $125^{2}$ + $6^{2}$ + $1^{2}$ + $1^{2}$
라는 해를 구하는데 8초가 걸렸다는 보고가 있다. 좀 더 어려운 문제에 대해서는 56초가 걸렸다: 11339 = $105^{2}$ + $15^{2}$ + $8^{2}$ + $5^{2}$
.

자연수  *n* 이 주어질 때,  *n* 을 최소 개수의 제곱수 합으로 표현하는 컴퓨터 프로그램을 작성하시오.

## 입력

입력은 표준입력을 사용한다. 입력은 자연수  *n* 을 포함하는 한 줄로 구성된다. 여기서, 1 ≤  *n*  ≤  **1,000,000,000,000,000,000** 이다.

## 출력

출력은 표준출력을 사용한다. 합이  *n* 과 같게 되는 제곱수들의 최소 개수를 첫째 줄에 출력한다.

둘째 줄에는, 제곱의 합이  *n* 과 같게 되는 수들을 첫째 줄에 출력한 갯수만큼 공백으로 구분하여 출력한다. 음의 정수는 출력해서는 안된다.

답이 여러개인 경우, 아무거나 출력해도 좋다.

## 예제

### 예제 입력 1

```
25
```

### 예제 출력 1

```
1
5
```

## 예제

### 예제 입력 2

```
26
```

### 예제 출력 2

```
2
1 5
```

## 예제

### 예제 입력 3

```
11339
```

### 예제 출력 3

```
3
1 27 103
```

## 예제

### 예제 입력 4

```
34567
```

### 예제 출력 4

```
4
1 22 109 149
```

## 출처

- 문제를 만든 사람: ho94949

## 알고리즘 분류

- 수학
- 정수론
- 소수 판정
- 소인수분해
- 밀러–라빈 소수 판별법
- 폴라드 로

def get_counts(n: int) -> int:
    # This function remains unchanged
    pass

# -------------------- Helpers for constructive representations --------------------

# Tonelli–Shanks for solving x^2 ≡ -1 (mod p), where p is an odd prime with p ≡ 1 (mod 4)
from random import randrange

def _tonelli_minus_one(p: int) -> int:
    """
    Return a solution r such that r^2 ≡ -1 (mod p), or 0 if trivial.
    Precondition: p is an odd prime with p % 4 == 1.
    """
    # Solve x^2 ≡ n (mod p) with n = p-1 (i.e., -1 mod p)
    n = p - 1
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1

    # find a quadratic non-residue z
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
        # find least i (0 < i < m) with t^(2^i) ≡ 1 (mod p)
        while t % p != 1:
            t = (t * t) % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m = i
        c = (b * b) % p
        t = (tt * c) % p
        r = (r * b) % p
    return r

def _cornacchia_two_squares_prime(p: int) -> tuple[int,int] | None:
    """
    Cornacchia's algorithm for x^2 + y^2 = p (prime p ≡ 1 mod 4).
    Returns (x, y) with x^2 + y^2 = p (x ≥ 0, y ≥ 0), or None if p ≡ 3 mod 4.
    """
    if p % 4 == 3:
        return None
    if p == 2:
        return (1, 1)  # 1^2 + 1^2 = 2

    r = _tonelli_minus_one(p)  # r^2 ≡ -1 (mod p)
    # Run the Euclidean algorithm on (p, r) until r^2 ≤ p
    a, b = p, r
    while b * b > p:
        a, b = b, a % b
    x2 = b * b
    y2 = p - x2
    return (b, int(y2 ** 0.5))

def _two_square_product(a: tuple[int,int], b: tuple[int,int]) -> tuple[int,int]:
    """
    (x1^2 + y1^2) * (x2^2 + y2^2) = (x1 x2 ± y1 y2)^2 + (x1 y2 ∓ y1 x2)^2
    We choose one sign to keep values small; order does not matter for the problem.
    """
    x1, y1 = a
    x2, y2 = b
    return (abs(x1 * x2 + y1 * y2), abs(x1 * y2 - y1 * x2))

def _factor_multiset(n: int) -> dict[int,int]:
    """Return prime factorization as {prime: exponent} using existing get_factors()."""
    from collections import Counter
    return Counter(get_factors(n))

def _square_part_and_core(n: int) -> tuple[int,int,dict[int,int]]:
    """
    Split n = mul^2 * core, where core is squarefree w.r.t. parity of exponents.
    Returns (mul, core, factors_dict)
    """
    fd = _factor_multiset(n)
    mul = 1
    core = 1
    for p, e in fd.items():
        mul *= p ** (e // 2)
        if e % 2 == 1:
            core *= p
    return mul, core, fd

def build_1(n: int) -> list[int]:
    # n is a perfect square
    from math import isqrt
    return [isqrt(n)]

def build_2(n: int) -> list[int]:
    """
    Construct a representation n = a^2 + b^2 when it exists (cnt == 2).
    Steps:
      1) n = mul^2 * core, where core is the product of primes with odd exponents.
      2) core's prime factors that are 1 mod 4 appear with odd exponent; primes 3 mod 4 must have even exponents.
      3) For each prime p ≡ 1 (mod 4) in the odd part, get (x,y) with x^2 + y^2 = p via Cornacchia.
      4) Multiply all (x,y) together via the two-square product, then scale by mul.
    """
    mul, core, fd = _square_part_and_core(n)

    # Collect primes with odd exponent and p ≡ 1 mod 4
    odd_one_mod_four = []
    for p, e in fd.items():
        if e % 2 == 1:
            if p % 4 == 1:
                odd_one_mod_four.append(p)
            else:
                # For cnt==2 branch this should not occur (Legendre two-square theorem)
                pass

    # Start with (1,0) then multiply in each prime representation
    x, y = 1, 0
    for p in odd_one_mod_four:
        sol = _cornacchia_two_squares_prime(p)
        assert sol is not None
        x, y = _two_square_product((x, y), sol)

    return [mul * x, mul * y]

def build_3(n: int) -> list[int]:
    """
    Construct n = a^2 + b^2 + c^2 when cnt == 3.
    Strategy:
      n = mul^2 * core, try t = 1,2,... such that core - t^2 has cnt == 2,
      then combine build_2(core - t^2) with t, and scale by mul.
    """
    mul, core, _ = _square_part_and_core(n)
    t = 1
    while True:
        if t * t > core:
            # Fallback (should not happen for valid cnt==3 cases)
            break
        if get_counts(core - t * t) == 2:
            a, b = build_2(core - t * t)
            return [mul * a, mul * b, mul * t]
        t += 1
    # Fallback (should be unreachable): naive search (slow for huge n)
    from math import isqrt
    for i in range(isqrt(n), 0, -1):
        m = n - i * i
        for j in range(isqrt(m), 0, -1):
            if is_square(m - j * j):
                return [i, j, isqrt(m - j * j)]

def build_4(n: int) -> list[int]:
    """
    Construct n = a^2 + b^2 + c^2 + d^2 (Lagrange).
    Use identity: if m = n / 4^ct (removing factors of 4),
    then represent m-1 as three squares and append 1; finally scale back by 2^ct.
    """
    ct = 0
    m = n
    while m % 4 == 0:
        m //= 4
        ct += 1
    # Represent m - 1 as sum of three squares, then add 1
    a, b, c = build_3(m - 1)
    scale = 1 << ct
    return [a * scale, b * scale, c * scale, scale]

def main():
    n = int(input())
    cnt = get_counts(n)
    print(cnt)
    match cnt:
        case 1:
            a = build_1(n)
            print(*a)
        case 2:
            a, b = build_2(n)
            print(a, b)
        case 3:
            a, b, c = build_3(n)
            print(a, b, c)
        case 4:
            a, b, c, d = build_4(n)
            print(a, b, c, d)
