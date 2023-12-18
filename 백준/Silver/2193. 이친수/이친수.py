n = int(input())
D = [[0, 0] for _ in range(n + 1)]
D[1] = [0, 1]

for i in range(2, n + 1):
    D[i][0] = sum(D[i - 1])
    D[i][1] = D[i - 1][0]

print(sum(D[n]))
