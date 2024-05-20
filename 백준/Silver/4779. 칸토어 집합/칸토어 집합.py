def cantor(n):
    if n == 0:
        return '-'
    
    return f'{cantor(n - 1)}{" " * (3**(n - 1))}{cantor(n - 1)}'

try:
    while True:
        n = int(input())
        print(cantor(n))
except:
    ...