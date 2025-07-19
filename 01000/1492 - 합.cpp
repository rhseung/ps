#include <bits/stdc++.h>
#define endl "\n"
#define MOD 1'000'000'007
using namespace std;

int dq[50][50];

long long int power(long long int m, int p, int mod) {
    if (p == 0) return 1;
    else if (p == 1) return m % mod;

    long long hp = power(m, p / 2, mod) % mod;
    return (hp * hp % mod) * power(m, p - 2 * (p / 2), mod) % mod;
}

long long int get_coeff(int n, int r) {
   if (dq[n][r] != 0) return dq[n][r];
    else if (n == 0) return 1;
    else if (n == r) return 1;
    else {
        dq[n][r] = ((n + 1) * (get_coeff(n, r - 1) % MOD) % MOD + get_coeff(n - 1, r - 1) % MOD) % MOD;
        return dq[n][r];
    }
}

long long int P(int n, int m) {
    if (m == 0) return 1;
    else return n * (P(n - 1, m - 1) % MOD) % MOD;
}

void solve() {
    int n, k;
    cin >> n >> k;

    long long int coeff[50] = { 0, };
    
    for (int i = 0; i < k; i++) {
        coeff[i] = get_coeff(k - i - 1, k - 1);
    }

    int ret = 0;

    // r^p == r <=> r^(p-1) == 1
    // a == ar^(p-1)
    // a/r == ar^(p-2) == ar^1'000'000'005
    for (int i = k + 1; i >= 2; i--) {
        long long int a = coeff[k + 1 - i] % MOD;
        long long int b = P(n + 1, i) % MOD;
        long long int c = (a * b) % MOD;
        long long int d = power(i, MOD - 2, MOD) % MOD;

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