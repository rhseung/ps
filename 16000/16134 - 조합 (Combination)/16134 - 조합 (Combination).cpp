// BOJ 16134 - 조합 (Combination)
#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

inline ll modpow(ll a, ll b, const ll c) {
    ll ret = 1;
    while (b) {
        if (b & 1) ret = ret * a % c;
        b >>= 1;
        a = a * a % c;
    }
    return ret;
}

/**
 * n을 radix 진법으로 변환하여 각 자리수를 반환하는 함수
 * @param number 변환할 숫자
 * @param radix 변환할 진법
 * @returns 각 자리수를 담은 벡터 - 주의: 뒤집혀서 저장됨.
 */
inline vector<ll> radix_convert(ll number, const ll radix) {
    vector<ll> digits;
    while (number > 0) {
        digits.push_back(number % radix);
        number /= radix;
    }
    return digits;
}

/**
 * 작은 이항 계수 계산 (nCk) (mod p)
 * @param n
 * @param k
 * @param mod prime number 일 때만 작동
 * @return
 */
inline ll binomial_coeff_small(const ll n, const ll k, const ll mod) {
    if (k < 0 || k > n)
        return 0; // nCk = 0 if k < 0 or k > n
    if (k == 0 || k == n)
        return 1;

    ll res = 1;

    for (ll i = 1; i <= k; ++i) {
        res = res * (n - i + 1) % mod;

        /**
         * 페르마의 소정리: a^(p-1) ≡ 1 (mod p) for prime p
         * 즉, a^(p-2) ≡ a^(-1) (mod p)
         */
        res = res * modpow(i, mod - 2, mod) % mod;
    }

    return res;
}

/**
 * Lucas의 정리: nCk (mod p) = (n1Ck1 * n2Ck2 * ... * nmCm) (mod p)
 * where n = n1 * p^0 + n2 * p^1 + ... + nm * p^(m-1), (p진법)
 * where k = k1 * p^0 + k2 * p^1 + ... + km * p^(m-1), (p진법)
 * @param n
 * @param k
 * @param mod prime number 일 때만 작동
 */
inline ll binomial_coeff(const ll n, const ll k, const ll mod) {
    const vector<ll> n_digits = radix_convert(n, mod);
    const vector<ll> k_digits = radix_convert(k, mod);

    ll res = 1;
    for (size_t i = 0; i < max(n_digits.size(), k_digits.size()); ++i) {
        const ll n_i = i < n_digits.size() ? n_digits[i] : 0;
        const ll k_i = i < k_digits.size() ? k_digits[i] : 0;

        res = res * binomial_coeff_small(n_i, k_i, mod) % mod;
    }

    return res;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    ll n, k;
    cin >> n >> k;
    cout << binomial_coeff(n, k, 1'000'000'007) << endl;

    return 0;
}
