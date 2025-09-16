# BOJ 10562 - 나이트
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

DP = [
    [ 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 73741815, 147483630, 294967260, 589934520, 179869031, 359738062, 719476124, 438952239, 877904478, 755808947, 511617885, 23235761, 46471522, 92943044, 185886088, 371772176, 743544352, 487088695, 974177390, 948354771, 896709533 ],
    [ 4, 16, 36, 81, 225, 625, 1600, 4096, 10816, 28561, 74529, 194481, 509796, 1336336, 3496900, 9150625, 23961025, 62742241, 164249856, 429981696, 125736695, 947295503, 716041218, 200652461, 886200432, 458408758, 488281642, 5232020, 529362765, 586008745, 223562643, 76425889, 19069136, 2388928, 953136135, 800450530, 539745896, 966886539, 121283871, 9235872, 533782787, 607200726, 645372102, 671380047, 668750842, 292390808, 950920440, 345351007, 557653218, 15148755 ],
    [ 8, 36, 94, 278, 1062, 3650, 11856, 39444, 135704, 456980, 1534668, 5166204, 17480600, 58888528, 198548648, 669291696, 258436230, 613387281, 676312919, 575341762, 991128221, 557546496, 284542480, 209398972, 232230803, 303596263, 939962513, 351290213, 415931359, 328520111, 887554940, 303667674, 351233655, 747600119, 130781946, 702928593, 155509746, 538853820, 548779965, 726903524, 370846848, 989333901, 795920339, 432839282, 815115627, 902444432, 3195020, 783730971, 232305131, 894592622 ],
    [ 16, 81, 278, 1365, 7164, 33858, 161307, 791722, 3859473, 18702843, 90938441, 442661923, 152542080, 466805482, 911253057, 627500238, 355979736, 651184968, 444168477, 637675570, 340713937, 193363675, 666524059, 932645942, 897647645, 834763352, 662912921, 725854997, 840822360, 61565774, 135123018, 995036230, 730107533, 462094335, 710509782, 525321589, 949550086, 8069878, 739604600, 955573146, 817055186, 27292242, 254984760, 388463753, 467535957, 483265312, 352974171, 592298092, 268922749, 66458109 ],
]

t = int(input())
bm = BerlekampMassey(10**9 + 9)

for _ in range(t):
    m, n = map(int, input().split())
    m -= 1
    n -= 1

    v = [DP[m][i] for i in range(50)]
    print(bm.guess_nth_term(v, n))