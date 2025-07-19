n = int(input())
D = [0] * (n + 1)
D[1] = 1
if n >= 2:
    D[2] = 2

for i in range(3, n + 1):
    D[i] = (D[i - 1] + D[i - 2]) % 10007    # note: 10007로 나누는 거 언제까지 까먹어ㅓㅓㅓㅓㅓ

print(D[n])
