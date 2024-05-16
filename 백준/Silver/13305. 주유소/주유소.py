n = int(input().strip())
dist = [0] + list(map(int, input().split()))
prices = list(map(int, input().split()))

oil = 0
price = 0

for i in range(n - 1):
    if oil < dist[i + 1]:
        if i + 2 < n and prices[i] < prices[i + 1]:
            price += prices[i] * (dist[i + 1] + dist[i + 2] - oil)
            oil = dist[i + 1] + dist[i + 2]
        else:
            price += prices[i] * (dist[i + 1] - oil)
            oil = dist[i + 1]
    oil -= dist[i + 1]

print(price)