#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using lnt = long long int;

#define MOD 1'000'000'007

lnt permutation(lnt n, lnt k) {
    lnt ret = 1;
    for (lnt i = 0; i < k; ++i)
        ret = ret * ((n - i) % MOD) % MOD;
    return ret;
}

lnt factorial(lnt n) {
    lnt ret = 1;
    for (lnt i = 1; i <= n; ++i)
        ret = ret * i % MOD;
    return ret;
}

lnt power(lnt n, lnt p) {
    if (p == 1) return n;
    else if (p == 0) return 1;

    lnt half = power(n, p / 2) % MOD;
    lnt half2 = half * half % MOD;
    return half2 * (p % 2 == 0 ? 1 : n % MOD) % MOD;
}

lnt divide(lnt x, lnt y) {
    // x/y mod M = ?
    // y^(M - 1) mod M = 1
    // y^(M - 2) mod M = 1/y
    // x*y^(M - 2) mod M = x/y

    return (x % MOD) * (power(y, MOD - 2) % MOD) % MOD;
}

void solution() {
    lnt n, k;
    cin >> n >> k;

    // nCk = nPk / k!
    cout << divide(permutation(n, k), factorial(k));
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
