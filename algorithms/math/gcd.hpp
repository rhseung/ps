//
// Created by Hyunseung Ryu on 2025. 7. 19..
//

#ifndef EUCLIDEAN_ALGORITHM_HPP
#define EUCLIDEAN_ALGORITHM_HPP

#include <tuple>

using namespace std;
typedef long long ll;

namespace math {

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

} // namespace math

#endif // EUCLIDEAN_ALGORITHM_HPP
