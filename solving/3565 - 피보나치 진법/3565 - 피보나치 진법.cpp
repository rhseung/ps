// BOJ 3565 - 피보나치 진법
#include <bits/stdc++.h>
using namespace std;

using u128 = unsigned __int128;
using u64 = unsigned long long;

struct DP {
    // count[n][prev1], sumOnesAll[n][prev1]
    // n: remaining length, prev1: was previous bit 1?
    static constexpr int MAXN = 95;
    unsigned long long cnt[ MAXN ][2]{};
    __int128 sum[ MAXN ][2]{};

    DP() {
        // base
        cnt[0][0] = cnt[0][1] = 1;
        sum[0][0] = sum[0][1] = 0;

        for (int n = 1; n < MAXN; ++n) {
            // prev1=false
            cnt[n][0] = cnt[n-1][0] + cnt[n-1][1];
            // choose 0: sum[n-1][0]
            // choose 1: +1 per string (cnt[n-1][0]) and then sum[n-1][1]
            sum[n][0] = sum[n-1][0] + (__int128)cnt[n-1][0] + sum[n-1][1];

            // prev1=true (must choose 0)
            cnt[n][1] = cnt[n-1][0];
            sum[n][1] = sum[n-1][0];
        }
    }

    // total ones among the first t strings (0 <= t <= cnt[n][prev1]), lex order
    __int128 sumFirstT(int n, unsigned long long t, int prev1) const {
        if (t == 0 || n == 0) return 0;
        unsigned long long c0 = cnt[n-1][0]; // choosing 0 now (prev1 becomes 0)
        if (prev1 == 1) {
            // can only choose 0
            return sumFirstT(n-1, t, 0);
        }
        if (t <= c0) {
            // all in 0-branch
            return sumFirstT(n-1, t, 0);
        } else {
            unsigned long long t1 = t - c0;
            // 0-branch fully + pick 1 now for t1 strings + recurse in (n-1, prev1=1)
            return sum[n-1][0] + (__int128)t1 + sumFirstT(n-1, t1, 1);
        }
    }

    // number of ones in the first m bits of the k-th string (0-based) of length n, lex order
    unsigned long long kthPrefixOnes(int n, unsigned long long k, int m, int prev1) const {
        unsigned long long ones = 0;
        for (int i = 0; i < m; ++i) {
            if (n == 0) break; // safety
            if (prev1 == 1) {
                // forced 0
                prev1 = 0;
                --n;
                continue;
            }
            unsigned long long c0 = cnt[n-1][0];
            if (k < c0) {
                // choose 0
                prev1 = 0;
                --n;
            } else {
                // choose 1
                k -= c0;
                ones += 1;
                prev1 = 1;
                --n;
            }
        }
        return ones;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    unsigned long long N;
    if (!(cin >> N)) return 0;
    if (N == 0) { cout << 0 << '\n'; return 0; }

    DP dp;

    // We iterate by Fibonacci-code length L = 1,2,3,...
    // For L=1: only "1" (F1=1), ones sum = 1, chars = 1
    // For L>=2: each code = "10" + free suffix of length n=L-2
    //   count of codes C_L = cnt[L-2][0] = F_L
    //   ones in whole block = C_L (leading 1s) + sum[n][0]
    __int128 answer = 0;
    unsigned long long remaining = N;

    for (int L = 1; ; ++L) {
        // compute block size and block ones
        u128 blockChars = 0;
        __int128 blockOnes = 0;

        if (L == 1) {
            unsigned long long C = 1; // only "1"
            blockChars = (u128)L * C; // 1
            blockOnes = 1;           // '1'
        } else if (L == 2) {
            unsigned long long C = 1; // only "10"
            blockChars = (u128)L * C; // 2
            blockOnes = 1;
        } else {
            int n = L - 2;
            unsigned long long C = dp.cnt[n][0]; // F_L
            blockChars = (u128)L * C;
            blockOnes = (__int128)C + dp.sum[n][0];
        }

        if (blockChars <= remaining) {
            // take whole block
            answer += blockOnes;
            remaining -= (unsigned long long)blockChars; // safe since remaining<=1e15
            if (remaining == 0) break;
        } else {
            // take partial inside this block
            if (L == 1) {
                // we can only take up to 1 char '1'
                answer += 1; // since remaining>=1 here
                remaining = 0;
                break;
            } else if (L == 2) {
                // block is "10"
                // remaining is 1 or 2
                if (remaining == 1) answer += 1; // '1'
                else answer += 1; // '10' has only one '1'
                remaining = 0;
                break;
            } else {
                int n = L - 2;
                unsigned long long C = dp.cnt[n][0];

                unsigned long long t = remaining / L; // full codes count
                unsigned long long r = remaining % L; // extra chars

                // add t full codes:
                // each has leading '1' -> +t
                answer += t;
                // plus ones among first t suffix strings (length n, prev1=false)
                answer += dp.sumFirstT(n, t, 0);

                // add r chars of the (t)-th code (0-based)
                if (r > 0) {
                    // code = "10" + suffix_k
                    // r==1: just '1'
                    // r==2: '10'
                    // r>=3: '10' + first (r-2) bits of kth suffix
                    unsigned long long add = 0;
                    if (r >= 1) add += 1;      // leading '1'
                    if (r >= 2) {/* +0 */}
                    if (r >= 3) add += dp.kthPrefixOnes(n, t, (int)r - 2, 0);
                    answer += add;
                }

                remaining = 0;
                break;
            }
        }
    }

    // answer <= N <= 1e15, so fits in 64-bit
    cout << (unsigned long long)answer << '\n';
    return 0;
}