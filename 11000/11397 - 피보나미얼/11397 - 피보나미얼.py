# BOJ 11397 - 피보나미얼
import sys

input = sys.stdin.readline


def sol(n, st, p):
    ans = 0
    if p == 2:
        ans += n // st
        st *= p
        while n // st:
            if st == 6:
                ans += n // st * 2
            else:
                ans += n // st
            st *= p
    else:
        while n // st:
            ans += n // st
            st *= p
    return ans


def f(n):
    ans = [0] * 1010
    while n % 2 == 0:
        n //= 2
        ans[2] += 1

    for i in range(3, int(n ** 0.5) + 1, 2):
        while n % i == 0:
            n //= i
            ans[i] += 1
        if n == 1:
            break
    if not n == 1:
        ans[n] += 1
    return ans


n, p = map(int, input().split())
num = [0] * 2000
prime = [2]
st = []

for i in range(3, int(1000 ** 0.5) + 1, 2):
    if num[i] or i % 2 == 0:
        continue
    for j in range(i * i, 1000, i):
        num[j] = 1

for i in range(3, 1000, 2):
    if num[i] == 0:
        prime.append(i)

for i in prime:
    a, b, cnt = 0, 1, 0
    while 1:
        s = a + b
        a = b
        b = s
        cnt += 1
        if s % i == 0:
            break
    st.append(cnt + 1)

for i in range(2, p + 1):
    ans = 1e9
    c = f(i)
    for j in range(2, i + 1):
        if c[j] == 0:
            continue
        ind = prime.index(j)
        ans = min(ans, sol(n, st[ind], j) // c[j])
    print(ans)
