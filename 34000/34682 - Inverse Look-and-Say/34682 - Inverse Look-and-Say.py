# BOJ 34682 - Inverse Look-and-Say
import sys
from collections import defaultdict


def input() -> str: return sys.stdin.readline().rstrip()

N = input()
if len(N) % 2 == 1:
    print(-1)
    sys.exit()

# 132112 -> 1개의 3, 2개의 1, 1개의 2 -> 3112
X = ""
for i in range(0, len(N), 2):
    cnt = int(N[i])
    val = N[i + 1]
    X += val * cnt

def f(x: str) -> str:
    # 3112 -> 132112
    # 1211 -> 111221

    N = ""
    freq = 1
    for i in range(1, len(x)):
        if x[i - 1] == x[i]:
            freq += 1
        else:
            N += f"{freq}{x[i - 1]}"
            freq = 1
    N += f"{freq}{x[-1]}"

    return N

# print(f"{N=}, {X=}, {f(X)=}")

if N != f(X):
    print(-1)
    sys.exit()

if X.startswith("0"):
    print(-1)
    sys.exit()

print(X)