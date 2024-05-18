n = int(input().strip())
dist = list(map(int, input().split()))
prices = list(map(int, input().split()))

price = 0
M = []
cursor = 0
val = 0

for i in range(n - 1):
    if prices[cursor] > prices[i]:
        price += prices[cursor] * val
        # M.append((cursor, val))
        cursor = i
        val = dist[i]
    else:
        val += dist[i] 
# M.append((cursor, val))
price += prices[cursor] * val

print(price)
# print(M)
