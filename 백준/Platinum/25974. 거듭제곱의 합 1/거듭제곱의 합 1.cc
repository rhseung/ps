#include <bits/stdc++.h>
#define endl "\n"
#define MOD 1'000'000'007
using lnt = long long int;
using namespace std;
#define MAX 1000
int dp[MAX][MAX] = { 0, };

lnt power(lnt m, int p, int mod) {
    if (p == 0) return 1;
    else if (p == 1) return m % mod;

    long long hp = power(m, p / 2, mod) % mod;
    return (hp * hp % mod) * power(m, p - 2 * (p / 2), mod) % mod;
}

lnt get_coeff(int n, int r) {
    if (dp[n][r] != 0) return dp[n][r];
    else if (n == 0) return 1;
    else if (n == r) return 1;
    else {
        dp[n][r] = ((n + 1) * (get_coeff(n, r - 1) % MOD) % MOD + get_coeff(n - 1, r - 1) % MOD) % MOD;
        return dp[n][r];
    }
}

lnt P(int n, int m) {
    if (m == 0) return 1;
    else return n * (P(n - 1, m - 1) % MOD) % MOD;
}

void solve() {
    int n, k;
    cin >> n >> k;

    if (k == 0) {
        cout << n;
        return;
    }

    lnt coeff[MAX] = { 0, };

    for (int i = 0; i < k; i++) {
        coeff[i] = get_coeff(k - i - 1, k - 1);
    }

    int ret = 0;

    // r^p == r <=> r^(p-1) == 1
    // a == ar^(p-1)
    // a/r == ar^(p-2) == ar^1'000'000'005
    for (int i = k + 1; i >= 2; i--) {
        lnt a = coeff[k + 1 - i] % MOD;
        lnt b = P(n + 1, i) % MOD;
        lnt c = (a * b) % MOD;
        lnt d = power(i, MOD - 2, MOD) % MOD;

        ret = (ret % MOD + (c * d) % MOD) % MOD;
    }

    cout << ret;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    // cout << fixed;
    // cout.precision(6);

    //int T; cin >> T; while (T--) 
    {
        solve();
    }

    return 0;
}