#include <bits/stdc++.h>
#define endl "\n"
#define INF 0x3f3f3f3f

using namespace std;
typedef long long ll;

/**
 * 확장 유클리드 호제법
 * @param a
 * @param b
 * @return ax + by = gcd(a, b) 를 만족하는 (x, y, gcd(a, b)) 튜플
 *  => Ax + By = C 형태의 방정식에서 A, B, C가 주어졌을 때 x, y를 구할 수 있음.
 * where C % gcd(A, B) == 0
 */
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

/**
 * ax + my = 1 => ax ≡ 1 (mod mod) => x는 a의 m에 대한 곱셈 역원
 * @param a
 * @param mod
 * @return a의 m에 대한 곱셈 역원, gcd(a, m) = 1일 때 존재
 */
ll multiplicative_inverse(const ll a, const ll mod) {
  ll inverse, gcd;
  tie(inverse, ignore, gcd) = extended_gcd(a, mod);

  if (gcd != 1)
    return -1;

  // 음수일 수도 있으므로 양수로 변환
  return (inverse % mod + mod) % mod;
}

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);
  cout.tie(nullptr);

  ll mod, a;
  cin >> mod >> a;

  const ll inv = multiplicative_inverse(a, mod);
  cout << (mod - a) << " " << inv << endl;

  return 0;
}