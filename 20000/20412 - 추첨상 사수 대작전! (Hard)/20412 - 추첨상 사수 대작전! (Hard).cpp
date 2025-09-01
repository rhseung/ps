// BOJ 20412 - 추첨상 사수 대작전! (Hard)
#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

/**
 * 페르마의 소정리 기반 a^-1 (mod m) 곱셈 역원 계산. O(log mod).
 * @note mod는 소수, gcd(a, mod) = 1.
 * @param a
 * @param mod
 */
ll fermat_inverse(ll a, const ll mod) {
    // a^(mod-2) % mod
    ll res = 1;
    ll exp = mod - 2;
    a %= mod;

    while (exp > 0) {
        if (exp & 1) res = res * a % mod;
        a = a * a % mod;
        exp >>= 1;
    }

    return res;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    ll m, seed, x1, x2;
    cin >> m >> seed >> x1 >> x2;

    // x1 = (a * seed + c) % m
    // x2 = (a * x1 + c) % m
    // x2 - x1 = a * (x1 - seed) % m
    // (x1-seed)*a ≡ (x2-x1) (mod m)

    const ll inverse_x1_seed = fermat_inverse(x1 - seed, m);
    const ll a = ((x2 - x1) % m * inverse_x1_seed % m + m) % m;
    const ll c = (x1 - a * seed % m + m) % m;
    cout << a << " " << c << endl;

    return 0;
}
