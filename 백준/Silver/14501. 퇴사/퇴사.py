N = int(input())
T = [0] * N
P = [0] * N
D = [0] * (N + 1)

for i in range(0, N):
    T[i], P[i] = map(int, input().split())

for i in range(N - 1, -1, -1):
    if i + T[i] <= N:
        D[i] = max(D[i + 1], D[i + T[i]] + P[i])   # 상담 스킵 or 상담 선택
    else:
        D[i] = D[i + 1]     # 상담 스킵

print(D[0])
