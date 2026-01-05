# BOJ 33622 - 새치기하지 마!!!
import sys
def input() -> str: return sys.stdin.readline().rstrip()

N = int(input())

# k1 + k2 + ... + kx = N
# 안 걸리고 새치기 할 확률 = (1 - k1/(N + 1)) * (1 - k2/(N + 1 - k1)) * (1 - k3/(N + 1 - k1 - k2)) * ... * (1 - kx/(N + 1 - k1 - ... - k{x-1}))
# = (N + 1 - k1)/(N + 1) * (N + 1 - k1 - k2)/(N + 1 - k1) * ... * (N + 1 - k1 - ... - kx)/(N + 1 - k1 - ... -k{x-1})
# = 1/(N + 1) * (N + 1 - k1 - ... - kx) = 1/(N + 1) * (N + 1 - N) = 1/(N + 1)

# k와 상관이 없다
# 그냥 k = N, x = 1로 출력하도록 하자

print(1)
print(N)
