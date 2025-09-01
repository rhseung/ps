// BOJ 13358 - Exponial
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

ll naive(const ll n, const ll m) {
    if (n == 1) return 1;
    else return modpow(n, naive(n - 1, m), m);
}

ll exponial(const ll n, const ll m) {
    // cout << "n: " << n << ", m: " << m << endl;
    if (m == 1) return 1; // 대신 마지막에 exponial(n, m) % m을 해줘야 함

    if (n <= 5) return naive(n, m);

    const ll p = phi(m);
    return modpow(n, exponial(n - 1, p) + p, m);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    // a^p mod m을 어떻게 구할 수 있을까?
    // 0 <= p < phi(m): a^p mod m을 fast pow로 로그 시간에 구할 수 있다.
    // phi(m) <= p: a^p = a^(p mod phi(m) + phi(m)) mod m을 이용해 구할 수 있다.
    // exponial(n) = n^exponial(n-1) = n^(n^(n-1)^(n-2)...(2^1)) 이므로
    // exponial(n) mod m = n^exponial(n-1) mod m = n^(exponial(n-1) mod phi(m) + phi(m)) mod m

    ll n, m;
    cin >> n >> m;
    cout << exponial(n, m) % m << endl;

    return 0;
}
