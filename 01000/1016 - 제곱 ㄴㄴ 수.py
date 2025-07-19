__problem__ = 'https://boj.kr/1016', '제곱 ㄴㄴ 수'

import sys

input = sys.stdin.readline

m, M = map(int, input().split())

# 에라토스테네스의 체를 응용하여 소수가 아니라 제곱 수의 배수를 소거하는 방법
count = M - m + 1
sieve = [True] * count

n = 2
while (square := n * n) <= M:

    mult = m // square
    while (num := mult * square) <= M:
        if m <= num <= M:
            if sieve[num - m]:
                sieve[num - m] = False
                count -= 1
        mult += 1

    n += 1

print(count)
