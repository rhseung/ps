// BOJ 4862 - 마지막 자리
#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

ll modpow(ll a, ll b, ll c) {
    ll ret = 1;
    while (b) {
        if (b & 1) ret = ret * a % c;
        b >>= 1;
        a = a * a % c;
    }
    return ret;
}

ll phi(ll n) {
    ll result = n;

    for (ll i = 2; i * i <= n; ++i) {
        if (n % i == 0) {
            result -= result / i;
            while (n % i == 0) n /= i;
        }
    }

    if (n > 1)
        result -= result / n;

    return result;
}

ll naive(const ll b, const ll x, const ll m) {
    if (x == 0) return 1;
    else return modpow(b, naive(b, x - 1, m), m);
}

ll f(const ll b, const ll x, const ll m) {
    if (m == 1) return 1; // 대신 마지막에 f(b, x, m) % m을 해줘야 함
    if (x == 0) return 1;
    if (x <= 5) return naive(b, x, m);

    // a^p = a^(p mod phi(m)) mod m을 이용해 구할 수 있다.
    const ll p = phi(m);
    return modpow(b, f(b, x - 1, p) + p, m);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    while (true) {
        int b, i, n;
        cin >> b;
        if (b == 0) break;
        cin >> i >> n;

        ll m = 1;
        for (int j = 0; j < n; j++) {
            m *= 10;
        }

        cout << setw(n) << setfill('0') << f(b, i, m) % m << endl;
    }

    return 0;
}
