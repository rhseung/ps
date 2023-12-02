n = int(input())
D = [[0] * 10 for _ in range(n+1)]
D[1][1:10] = [1] * 9

for i in range(2, n+1):
    for j in range(0, 9+1):
        if j == 0:
            D[i][j] = D[i-1][j+1]
        elif j == 9:
            D[i][j] = D[i-1][j-1]
        else:
            D[i][j] = (D[i-1][j-1] + D[i-1][j+1]) % 1000000000

print(sum(D[n]) % 1000000000)
