#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using lnt = long long int;

#define MOD 1000000007
lnt fact[4000001];

lnt fast_pow(lnt n, int p) {
    if (p == 0) return 1;
    else if (p == 1) return n % MOD;

    lnt half = fast_pow(n, p / 2);
    lnt half2 = (lnt)half * half % MOD;
    lnt remain = p % 2 == 0 ? 1 : n % MOD;

    return half2 * remain % MOD;
}

lnt binomial(int n, int k) {
    // (a/b) mod M = (a*b^(M-2)) mod M
    lnt nume = fact[n];
    lnt deno = (lnt)fact[k] * fact[n - k];

    return nume * fast_pow(deno, MOD - 2) % MOD;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int m;
    cin >> m;

    fact[0] = 1;
    for (int i = 1; i <= 4000000; ++i)
        fact[i] = fact[i - 1] * i % MOD;

    while (m--) {
        int n, k;
        cin >> n >> k;
        cout << binomial(n, k) << endl;
    }
}
