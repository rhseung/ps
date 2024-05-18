#include <bits/stdc++.h>
#define endl '\n'
#define MOD 1'000'000'007
using namespace std;
using i64 = int64_t;

i64 fast_pow(int d, int p, int mod) {
    if (p == 0) return 1;
    else if (p == 1) return d % mod;

    i64 half = fast_pow(d, p / 2, mod);
    i64 rest = fast_pow(d, p % 2, mod);

    i64 half2 = ((i64)half * half) % mod;
    return (half2 * rest) % mod;
}

i64 div(int a, int b, int mod) {
    // b^(m - 1) === 1
    // b^(m - 2) === 1/b
    // a*b^(m - 2) === a/b
    return (((i64)a % mod) * fast_pow(b, mod - 2, mod)) % mod;
}

void $(int m, int* N, int* S) {
    i64 sum = 0;

    for (int i = 0; i < m; ++i) {
        if (S[i] % N[i] == 0)
            sum = (sum + (S[i] / N[i]) % MOD) % MOD;
        else
            sum = (sum + div(S[i], N[i], MOD)) % MOD;
    }

    cout << sum;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int m;
    cin >> m;

    int* N = new int[m];
    int* S = new int[m];

    for (int i = 0; i < m; ++i)
        cin >> N[i] >> S[i];

    $(m, N, S);

    delete[] N;
    delete[] S;
}
