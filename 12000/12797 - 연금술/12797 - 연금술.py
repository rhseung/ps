# BOJ 12797 - 연금술
import sys
input = sys.stdin.readline

class BerlekampMassey:
    def __init__(self, mod: int = 998244353):
        self.mod = mod

    def berlekamp_massey(self, x: list[int]) -> list[int]:
        MOD = self.mod
        ls: list[int] = []
        cur: list[int] = []
        lf = -1
        ld = 1

        for i in range(len(x)):
            t = 0
            for j in range(len(cur)):
                t = (t + x[i - j - 1] * cur[j]) % MOD
            if (t - x[i]) % MOD == 0:
                continue

            if not cur:
                cur = [0] * (i + 1)
                lf = i
                ld = (t - x[i]) % MOD
                continue

            k = (-(x[i] - t)) * pow(ld, MOD - 2, MOD) % MOD
            c = [0] * (i - lf - 1)
            c.append(k)
            for coeff in ls:
                c.append((-coeff * k) % MOD)

            if len(c) < len(cur):
                c += [0] * (len(cur) - len(c))

            for j in range(len(cur)):
                c[j] = (c[j] + cur[j]) % MOD

            if i - lf + len(ls) >= len(cur):
                ls, lf, ld = cur, i, (t - x[i]) % MOD

            cur = c

        cur = [(v % MOD + MOD) % MOD for v in cur]
        return cur

    @staticmethod
    def _poly_mul_mod(v: list[int], w: list[int], rec: list[int], MOD: int) -> list[int]:
        m = len(v)
        t = [0] * (2 * m)
        for j in range(m):
            for k in range(m):
                t[j + k] = (t[j + k] + v[j] * w[k]) % MOD

        for j in range(2 * m - 1, m - 1, -1):
            if t[j] == 0:
                continue
            for k in range(1, m + 1):
                t[j - k] = (t[j - k] + t[j] * rec[k - 1]) % MOD

        return t[:m]

    def get_nth(self, rec: list[int], dp: list[int], n: int) -> int:
        MOD = self.mod
        m = len(rec)
        if n < len(dp):
            return dp[n] % MOD

        s = [0] * m
        t = [0] * m
        s[0] = 1
        if m != 1:
            t[1] = 1
        else:
            t[0] = rec[0]

        while n:
            if n & 1:
                s = self._poly_mul_mod(s, t, rec, MOD)
            t = self._poly_mul_mod(t, t, rec, MOD)
            n >>= 1

        ret = 0
        for i in range(m):
            ret = (ret + s[i] * dp[i]) % MOD
        return ret

    def guess_nth_term(self, seq: list[int], n: int) -> int:
        MOD = self.mod
        if n < len(seq):
            return seq[n] % MOD

        rec = self.berlekamp_massey(seq)
        if not rec:
            return 0

        m = len(rec)
        dp = [x % MOD for x in seq[:m]]
        return self.get_nth(rec, dp, n) % MOD

n, m = map(int, input().split())
A = list(map(int, input().split()))
mod = 10**9 + 7

DP = [[0] * m for _ in range(2*m)]
DP[0][0] = A[0]

# DP[i][j] = DP[i - 1][j] * A[j] + DP[i][j - 1]
for i in range(1, m):
    DP[0][i] = (DP[0][i - 1] + A[i]) % mod
for i in range(1, 2*m):
    DP[i][0] = (DP[i - 1][0] * A[0]) % mod
for j in range(1, m):
    for i in range(1, 2*m):
        DP[i][j] = (DP[i - 1][j] * A[j] + DP[i][j - 1]) % mod

rec = []
for i in range(0, 2*m):
    rec.append(DP[i][m - 1])

bm = BerlekampMassey(mod=mod)
print(bm.guess_nth_term(rec, n - 1))