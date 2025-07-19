n, k = map(int, input().split())
A = [int(input()) for _ in range(n)]

cnt = 0
for i in range(n - 1, -1, -1):
    e, k = divmod(k, A[i])
    cnt += e

print(cnt)
