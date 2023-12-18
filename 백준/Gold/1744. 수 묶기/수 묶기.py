n = int(input())
pos = []
neg = []
has_zero = False

s = 0
for i in range(n):
    x = int(input())

    if x == 1:
        s += x
    elif x == 0:
        has_zero = True
    elif x > 0:
        pos.append(x)
    else:
        neg.append(-x)  # note: 양수로 넣지 않는다면 sort 시 [-1, -2, -3, ...] 가 아니라 [..., -3, -2, -1] 가 됨

pos.sort()
neg.sort()

while len(pos) >= 2:
    s += pos.pop() * pos.pop()

while len(neg) >= 2:
    s += neg.pop() * neg.pop()

if pos:
    s += pos.pop()

if neg and not has_zero:
    s += -neg.pop()

print(s)
