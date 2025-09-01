#include <bits/stdc++.h>
#define endl "\n"
#define INF 0x3f3f3f3f

using namespace std;
typedef long long ll;

ll fast_power(const ll base, const ll exp, const ll mod) {
  if (exp == 0)
    return 1;
  if (exp == 1)
    return base % mod;

  const ll half = fast_power(base, exp / 2, mod);
  return (half * half % mod) * fast_power(base, exp - 2 * (exp / 2), mod) % mod;
}

vector<ll> radix_convert(ll number, const ll radix) {
  vector<ll> digits;
  while (number > 0) {
    digits.push_back(number % radix);
    number /= radix;
  }
  return digits;
}

ll binomial_coeff_small(const ll n, const ll k, const ll mod) {
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
    res = res * fast_power(i, mod - 2, mod) % mod;
  }

  return res;
}

ll binomial_coeff(const ll n, const ll k, const ll mod) {
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

tuple<ll, ll, ll> extended_gcd(const ll a, const ll b) {
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

ll multiplicative_inverse(
    const ll a, const ll mod, const function<ll()> &fallback = []() {
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

ll chinese_remainder_theorem(const vector<ll> &a, const vector<ll> &m) {
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

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);
  cout.tie(nullptr);

  int T;
  cin >> T;

  while (T--) {
    int n, m;
    cin >> n >> m;

    ll res;

    if (n == 0 && m == 1) {
      res = 1;
    } else if (n == 0 && m > 1) {
      res = 0;
    } else if (n > 0 && m == 1) {
      res = 0;
    } else { // n > 0 && m > 1 <=> n >= 1 && m >= 2
      // m-1Hn-(m-1) = n-1Cn-(m-1) = n-1Cm-2
      // 100007 = 97 * 1031
      ll m97 = binomial_coeff(n - 1, m - 2, 97);
      ll m1031 = binomial_coeff(n - 1, m - 2, 1031);

      res = chinese_remainder_theorem({m97, m1031}, {97, 1031});
    }

    cout << res << endl;
  }

  return 0;
}