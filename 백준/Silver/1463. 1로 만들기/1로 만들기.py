n = int(input())
D = {1: 0}

def get(n):
    if n not in D:
        if n % 6 == 0:
            D[n] = min(get(n // 2), get(n // 3)) + 1
        elif n % 2 == 0:
            D[n] = min(get(n - 1), get(n // 2)) + 1
        elif n % 3 == 0:
            D[n] = min(get(n - 1), get(n // 3)) + 1
        else:
            D[n] = get(n - 1) + 1
    
    return D[n]

print(get(n))
