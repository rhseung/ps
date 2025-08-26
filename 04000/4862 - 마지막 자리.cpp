// BOJ 4862 - 마지막 자리
#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

/**
 * 유클리드 호제법
 * @param a
 * @param b
 * @return gcd(a, b)
 */
inline ll gcd(const ll a, const ll b) {
    if (b == 0)
        return a;

    return gcd(b, a % b);
}

ll mod_nonzero(const ll a, const ll b) {
    return a > b ? a % b + b : a;
}

ll modpow(ll a, ll b, ll c) {
    ll ret = 1;
    while (b) {
        if (b & 1) ret = mod_nonzero(ret * a, c);
        b >>= 1;
        a = mod_nonzero(a * a, c);
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

ll f(const ll b, const ll x, const ll m) {
    if (x == 0) return 1;

    // a^p = a^(p mod phi(m)) mod m을 이용해 구할 수 있다.
    const ll p = phi(m);
    return modpow(b, f(b, x - 1, p), m);
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
