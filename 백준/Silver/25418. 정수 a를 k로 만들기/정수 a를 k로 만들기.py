import sys
inf = sys.maxsize

a, k = map(int, input().split())

def min_operation(a: int, k: int) -> int:
    D = [inf] * (k + 1)
    D[a] = 0
    
    for i in range(a + 1, k + 1):
        if i % 2 != 0:
            D[i] = D[i - 1] + 1
        else:
            D[i] = min(D[i - 1], D[i // 2]) + 1
    
    return D[k]

print(min_operation(a, k))