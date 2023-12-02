n = int(input())
D = {1: 1, 2: 2}

for i in range(3, n + 1):
    D[i] = (D[i - 1] + D[i - 2]) % 10007

print(D[n])
