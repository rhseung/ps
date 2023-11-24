__problem__ = 'https://boj.kr/1744', '수 묶기'

import sys

input = sys.stdin.readline

# 0은 음수랑 곱해서 소멸시키기
#  - [-5 -4 0] 에서 0은 오히려 곱하는게 안 좋음. 0은 모든 음수들을 다 곱하게 둔 뒤 홀수 개라 음수가 하나 남으면 그 때 0과 곱해주기
# 1은 그냥 더해. 1*n = n < 1+n 이기 때문.
# 나머지는 (최대*최대-1) 로?

n = int(input().strip())
pos = []
neg = []
zero = False
s = 0

for _ in range(n):
    tmp = int(input().strip())

    if tmp > 0:
        if tmp == 1:
            s += 1
        else:
            pos.append(tmp)
    elif tmp < 0:
        neg.append(-tmp)
    else:
        zero = True

pos.sort()
neg.sort()

while len(pos) > 1:
    s += pos.pop() * pos.pop()

if pos:
    s += pos.pop()

while len(neg) > 1:
    s += neg.pop() * neg.pop()

if neg and not zero:
    s += -neg.pop()     # neg는 양수로 저장되어있음 주의

print(s)
