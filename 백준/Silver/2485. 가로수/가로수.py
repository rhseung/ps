def gcd(a, b):
	if b == 0: return a
	else: return gcd(b, a % b)

n = int(input())
arr = []
sub = []
g = 1
plant = 0

for i in range(n):
	arr.append(int(input()))

	if i >= 1:
		sub.append(arr[i] - arr[i - 1])
		g = sub[i - 1] if i == 1 else gcd(g, sub[i - 1])

for e in sub:
	plant += (e // g) - 1

print(plant)