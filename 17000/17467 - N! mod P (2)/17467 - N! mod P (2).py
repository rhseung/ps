# BOJ 17467 - N! mod P (2)
import sys
input = sys.stdin.readline

n, mod = map(int, input().split())

r = mod - 1 - n

if n <= r:
    a = 1
    for i in range(2, n + 1):
        a = a * i % mod
    print(a)
else:
    a = 1
    for i in range(2, r + 1):
        a = a * i % mod
    
    inv = pow(a, mod - 2, mod)
    
    if (r & 1) < 1:
        print((-inv) % mod)
    else:
        print(inv)
