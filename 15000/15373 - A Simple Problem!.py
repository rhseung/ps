# BOJ 15373 - A Simple Problem!
import sys

input = sys.stdin.readline

P = [0] * 400001

for i in range(2, 701):
    if P[i] == 0:
        j = i
        while i * j <= 400000:
            P[i * j] = 1
            j += 1

Q = []
for i in range(2, 700):
    if P[i] == 0:
        Q.append(i)

A = [0] * 400001
B = [0] * 400001
Ans = [0] * 200001
Ans[1] = 1

a = 0
b = 1
for i in range(2, 200001):
    j = i
    for num in Q:
        cnt = 0
        while j % num == 0:
            cnt += 1
            j //= num

        A[num] += cnt
        if A[num] * 2 > B[num]:
            a += 1

    if j > 1:
        A[j] += 1
        if A[j] * 2 > B[j]:
            a += 1

    while True:
        if a == 0: Ans[i] = b; break
        b += 1
        c = b

        for num in Q:
            cnt = 0
            while c % num == 0:
                cnt += 1
                c //= num

            if B[num] < A[num] * 2 <= B[num] + cnt:
                a -= 1
            B[num] += cnt

        if c > 1:
            if B[c] < A[c] * 2 <= B[c] + 1:
                a -= 1
            B[c] += 1

for _ in range(int(input())):
    print(Ans[int(input())])
