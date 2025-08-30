// BOJ 19124 - Binomial Coefficient
#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

constexpr ull MOD = 1ull << 32; // 2^32
static constexpr ull BLOCK = 1ull << 16; // 65536

inline ull mask_t(unsigned t) {
    return (t == 64 ? ~0ull : ((1ull << t) - 1ull));
}

inline ull mul_pow2(ull a, ull b, unsigned t) {
    return (a * b) & mask_t(t);
}

inline ull pow_pow2(ull a, ull e, unsigned t) {
    ull m = mask_t(t);
    ull r = 1ull & m;
    a &= m;
    while (e) {
        if (e & 1ull) r = (r * a) & m;
        e >>= 1ull;
        a = (a * a) & m;
    }
    return r;
}

// cache FULL[t] = product_{i=1,3,5,...,BLOCK-1} i  (mod 2^t)
inline ull full_block_prod(unsigned t) {
    static ull cache[65]; // up to 64 just in case
    if (cache[t]) return cache[t];
    ull m = mask_t(t);
    ull full = 1ull & m;
    for (ull i = 1; i < BLOCK; i += 2ull) {
        full = (full * i) & m;
    }
    cache[t] = full;
    return full;
}

// odd_part_fact(n) modulo 2^t
inline ull odd_factorial_mod_2pow(ull n, unsigned t) {
    if (n == 0ull) return 1ull & mask_t(t);
    ull res = odd_factorial_mod_2pow(n >> 1, t);
    ull h = n / BLOCK;
    ull l = n % BLOCK;

    // multiply FULL^h
    ull full = full_block_prod(t);
    res = mul_pow2(res, pow_pow2(full, h, t), t);
    // multiply odds in the last partial block: (h*BLOCK + 1), (h*BLOCK + 3), ..., (h*BLOCK + l') with l' same parity as l
    ull now = 1ull & mask_t(t);
    ull b = h * BLOCK;

    for (ull i = 1; i <= l; i += 2ull) {
        now = mul_pow2(now, (b + i), t); // (b+i) is odd because BLOCK is 2^16 and i is odd
    }

    return mul_pow2(res, now, t);
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
 * @return a의 m에 대한 곱셈 역원, gcd(a, m) = 1일 때 존재
 */
inline ll multiplicative_inverse(const ll a, const ll mod) {
    ll inverse, gcd;
    tie(inverse, ignore, gcd) = extended_gcd(a, mod);

    if (gcd != 1)
        throw runtime_error("Multiplicative Inverse: inverse does not exist");

    // 음수일 수도 있으므로 양수로 변환
    return (inverse % mod + mod) % mod;
}

// nCk (mod 2^32) = 2^e * g(n) / (g(k) * g(n-k)) (mod 2^32)
inline ull binom_mod_2pow32(const ll n, const ll k) {
    if (k < 0 || k > n) return 0;
    const ll e = static_cast<ll>(__builtin_popcountll(k) + __builtin_popcountll(n - k) - __builtin_popcountll(n));
    if (e >= 32) return 0; // divisible by 2^32

    const unsigned t = static_cast<unsigned>(32 - e);
    const ull gn = odd_factorial_mod_2pow(static_cast<ull>(n), t);
    const ull gk = odd_factorial_mod_2pow(static_cast<ull>(k), t);
    const ull gnk = odd_factorial_mod_2pow(static_cast<ull>(n - k), t);

    const ull MOD_t = (1ull << t);
    const ull inv_gk = static_cast<ull>(multiplicative_inverse(static_cast<ll>(gk % MOD_t), static_cast<ll>(MOD_t)));
    const ull inv_gnk = static_cast<ull>(multiplicative_inverse(static_cast<ll>(gnk % MOD_t), static_cast<ll>(MOD_t)));
    ull tmp = (((gn % MOD_t) * inv_gk) % MOD_t);
    tmp = (tmp * inv_gnk) % MOD_t;
    // lift: multiply by 2^e under mod 2^32
    ull res = (tmp << e) % MOD;
    return res;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    ll n, k;
    cin >> n >> k;
    const ull m2_32 = binom_mod_2pow32(n, k);
    cout << m2_32 << endl;

    return 0;
}
