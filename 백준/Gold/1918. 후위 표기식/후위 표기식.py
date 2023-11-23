__problem__ = 'https://boj.kr/1918', '후위 표기식'

import sys

input = sys.stdin.readline

expr = input().strip()

prior = {
    '+': 0,
    '-': 0,
    '*': 1,
    '/': 1
}
S = []
R = []

for c in expr:
    if c.isalpha():
        R.append(c)
    elif c in prior.keys():
        p = prior[c]

        while S and S[-1] in prior.keys() and prior[S[-1]] >= p:
            R.append(S.pop())

        S.append(c)
    elif c == '(':
        S.append(c)
    elif c == ')':
        while S[-1] != '(':
            R.append(S.pop())

        S.pop()

while S:
    R.append(S.pop())

print(*R, sep='')
