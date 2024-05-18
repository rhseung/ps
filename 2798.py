n, m = map(int, input().split())
A = list(map(int, input().split()))

min_diff = m

for i in range(n):
    for j in range(i + 1, n):
        for k in range(j + 1, n):
            if A[i] + A[j] + A[k] <= m and min_diff > m - (A[i] + A[j] + A[k]):
                min_diff = m - (A[i] + A[j] + A[k])

print(m - min_diff)
