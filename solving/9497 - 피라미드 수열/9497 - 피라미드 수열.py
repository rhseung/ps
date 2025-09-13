# BOJ 9497 - 피라미드 수열
import sys
from math import gcd

input = sys.stdin.readline

n, m = map(int, input().split())

g = gcd(2*n - 2, 2*m - 2)

qN, rN = divmod(n, g)
qM, rM = divmod(m, g)

C_same = g * qN * qM + qN * rM + qM * rN + (rN if rN < rM else rM)

if rN == 0 or rM == 0:
    T = 0
else:
    s = rN + rM - g
    T = s if s > 1 else 1
C_opp = g * qN * qM + qN * rM + qM * rN + T

A0 = qN + (1 if rN > 0 else 0)
B0 = qM + (1 if rM > 0 else 0)
C_both = A0 * B0
if g % 2 == 0:
    r = g // 2
    Ar = qN + (1 if rN > r else 0)
    Br = qM + (1 if rM > r else 0)
    C_both += Ar * Br

print(C_same + C_opp - C_both)
