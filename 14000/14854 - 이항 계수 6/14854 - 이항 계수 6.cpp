// BOJ 14854 - 이항 계수 6.cpp
#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

inline ll modmul(const ll a, const ll b, const ll m) {
    return static_cast<ll>(static_cast<__int128>(a) * b % m);
}

inline ll modpow(ll a, ll b, const ll m) {
    ll ret = 1;
    while (b) {
        if (b & 1) ret = ret * a % m;
        b >>= 1;
        a = a * a % m;
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

/**
 * 확장 유클리드 호제법, Extended Euclidean Algorithm (EEA)
 * @param a
 * @param b
 * @return ax + by = gcd(a, b) 를 만족하는 (x, y, gcd(a, b)) 튜플
 *  => Ax + By = C 형태의 방정식에서 A, B, C가 주어졌을 때 x, y를 구할 수 있음.
 * where C % gcd(A, B) == 0
 */
inline tuple<ll, ll, ll> extended_gcd(const ll a, const ll b) {
    if (a == b)
        return {1, 0, a};
    if (b == 0)
        return {1, 0, a};

    ll x_1 = 1, y_1 = 0, r_1 = a;
    ll x_2 = 0, y_2 = 1, r_2 = b;

    while (r_2 != 0) {
        const ll q = r_1 / r_2;

        const ll r_t = r_1 - q * r_2;
        const ll x_t = x_1 - q * x_2;
        const ll y_t = y_1 - q * y_2;

        x_1 = x_2;
        y_1 = y_2;
        r_1 = r_2;
        x_2 = x_t;
        y_2 = y_t;
        r_2 = r_t;
    }

    return {x_1, y_1, r_1};
}

/**
 * ax + my = 1 => ax ≡ 1 (mod m) => x는 a의 m에 대한 곱셈 역원
 * @param a
 * @param mod
 * @param fallback 곱셈 역원이 존재하지 않을 때 호출되는 함수
 * @return a의 m에 대한 곱셈 역원, gcd(a, m) = 1일 때 존재
 */
inline ll multiplicative_inverse(
    const ll a, const ll mod, const function<ll()>& fallback = []() {
        throw invalid_argument("Multiplicative inverse does not exist");
        return -1;
    }) {
    ll inverse, gcd;
    tie(inverse, ignore, gcd) = extended_gcd(a, mod);

    if (gcd != 1)
        return fallback();

    // 음수일 수도 있으므로 양수로 변환
    return (inverse % mod + mod) % mod;
}

/**
 * 중국인의 나머지 정리 (Chinese Remainder Theorem)
 * x ≡ a_1 (mod m_1), x ≡ a_2 (mod m_2), ..., x ≡ a_n (mod m_n) 형태에서
 * 서로 모두 서로소인 m_i들에 대해 x mod M (M = m_1 * m_2 * ... * m_n)를
 * 구합니다.
 * @param a 나머지들, 서로 다른 양의 정수들
 * @param m 모듈로들, 서로 서로소인 양의 정수들
 * @return x mod M, 여기서 M은 m의 곱입니다.
 * @note a와 m의 크기는 같아야 하고, m[i]는 서로 서로소여야 합니다.
 */
inline ll chinese_remainder_theorem(const vector<ll>& a, const vector<ll>& m) {
    assert(a.size() == m.size() &&
        "Chinese Remainder Theorem: a and m must have the same size");

    ll M = 1;
    for (const ll mod : m) {
        M *= mod;
    }

    ll result = 0;
    for (size_t i = 0; i < a.size(); ++i) {
        // N_i * inv_i ≡ 1 (mod m[i])
        const ll N_i = M / m[i];
        const ll inv_i = multiplicative_inverse(N_i, m[i]);

        // x += a_i * N_i * inv_i (mod M)
        result = (result % M + a[i] % M * N_i * inv_i % M) % M;
    }

    return result;
}

/**
 * v_3(n!) = n!의 소인수분해 시 3의 지수
 * v_3(n!) = n/3 + n/9 + n/27 + ...
 */
inline ll v3_fact(ll n) {
    ll s = 0;
    while (n) {
        n /= 3;
        s += n;
    }
    return s;
}

// g(x) = x!에서 3의 배수를 제거한 값 = x! / 3^e (mod 27) where e = v_3(x!)
// nCk = n! / (k! * (n-k)!) = 3^e * g(n) / (g(k) * g(n-k)) (mod 27) where e = v_3(n!) - v_3(k!) - v_3((n-k)!)
// g(x) = product{i / 3^v3(i) | 1 <= i <= x} = g(x / 3) * (1..x 중 3배수가 아닌 수의 곱) (mod 27)
// (1..x 중 3배수가 아닌 수의 곱) = A[x % 27] * U^(x / 27) (mod 27) where A[t] = product_{1<=i<=t, 3∤i} i (mod 27), U = A[26] = product of 1..27 excluding multiples of 3 (mod 27)
// g(x) = g(x / 3) * A[x % 27] * U^(x / 27) (mod 27)
inline ll g_mod27(const ll x) {
    if (x == 0) return 1;

    static bool inited = false;
    static ll A[27];
    static ll U;
    if (!inited) {
        A[0] = 1;
        for (int t = 1; t <= 26; ++t) {
            const ll v = (t % 3 == 0) ? 1 : t;
            A[t] = (A[t - 1] * v) % 27;
        }

        U = A[26]; // equals -1 mod 27
        inited = true;
    }

    // g(x) = g(x / 3) * A[x % 27] * U^(x / 27) (mod 27)
    return modmul(modmul(g_mod27(x / 3), A[x % 27], 27), modpow(U, x / 27, 27), 27);
}

// nCk (mod 27) = 3^e * g(n) / (g(k) * g(n-k)) (mod 27)
inline ll binom_mod_27(const ll n, const ll k) {
    if (k < 0 || k > n) return 0;
    const ll e = v3_fact(n) - v3_fact(k) - v3_fact(n - k);
    if (e >= 3) return 0; // 3^3으로 나눠떨어지므로 바로 0 반환

    const ll gn = g_mod27(n);
    const ll gk = g_mod27(k);
    const ll gnk = g_mod27(n - k);
    const ll inv_gk = multiplicative_inverse(gk, 27);
    const ll inv_gnk = multiplicative_inverse(gnk, 27);

    ll res = modmul(gn, modmul(inv_gk, inv_gnk, 27), 27);

    if (e == 1) res = modmul(res, 3, 27);
    else if (e == 2) res = modmul(res, 9, 27);
    return res;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        ll n, k;
        cin >> n >> k;

        ll m27 = binom_mod_27(n, k);
        ll m11 = binomial_coeff(n, k, 11);
        ll m13 = binomial_coeff(n, k, 13);
        ll m37 = binomial_coeff(n, k, 37);

        const ll m142857 = chinese_remainder_theorem({m27, m11, m13, m37}, {27, 11, 13, 37});
        cout << m142857 << endl;
    }

    return 0;
}
