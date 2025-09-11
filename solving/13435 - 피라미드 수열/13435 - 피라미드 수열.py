# BOJ 13435 - 피라미드 수열
import sys
from math import gcd

input = sys.stdin.readline

def count_distinct_pairs(N: int, M: int) -> int:
    # Period gcd
    g = gcd(2*N - 2, 2*M - 2)

    qN, rN = divmod(N, g)
    qM, rM = divmod(M, g)

    # C_same
    C_same = g*qN*qM + qN*rM + qM*rN + (rN if rN < rM else rM)

    # C_opp overlap term T
    if rN == 0 or rM == 0:
        T = 0
    else:
        s = rN + rM - g
        T = s if s > 1 else 1  # max(1, rN + rM - g)
    C_opp = g*qN*qM + qN*rM + qM*rN + T

    # C_both (r=0 and, if even g, r=g/2)
    A0 = qN + (1 if rN > 0 else 0)
    B0 = qM + (1 if rM > 0 else 0)
    C_both = A0 * B0
    if g % 2 == 0:
        r = g // 2
        Ar = qN + (1 if rN > r else 0)
        Br = qM + (1 if rM > r else 0)
        C_both += Ar * Br

    return C_same + C_opp - C_both



def main():
    n, m = map(int, input().split())
    print(count_distinct_pairs(n, m))

if __name__ == "__main__":
    main()
