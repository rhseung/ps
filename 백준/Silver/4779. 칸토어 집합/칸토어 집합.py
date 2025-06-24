def cantor(n):
    if n == 0:
        return '-'
    
    l = cantor(n - 1)
    return f'{l}{" " * (3**(n - 1))}{l}'

try:
    while True:
        n = int(input())
        print(cantor(n))
except:
    ...