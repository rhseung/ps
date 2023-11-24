__problem__ = 'https://boj.kr/1541', '잃어버린 괄호'

import sys

input = sys.stdin.readline

E = input().split('-')
# 가장 처음과 마지막 문자는 숫자이다 -> `-30-20` 같은 수식은 없으므로 항상 첫 번째는 수임.
result = sum(map(int, E[0].split('+')))

for i in range(1, len(E)):
    result -= sum(map(int, E[i].split('+')))

print(result)
