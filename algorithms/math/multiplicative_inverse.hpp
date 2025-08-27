//
// Created by Hyunseung Ryu on 2025. 7. 19..
//

#ifndef MULTIPLICATIVE_INVERSE_HPP
#define MULTIPLICATIVE_INVERSE_HPP

#include "gcd.hpp"

#include <functional>
#include <stdexcept>
#include <tuple>

using namespace std;
typedef long long ll;

namespace math {
  /**
   * 확장 유클리드 알고리즘을 이용한 ax ≡ 1 (mod m)일 때의 x의 a의 m에 대한 곱셈 역원 계산. O(log mod).
   * @note gcd(a, mod) = 1일 때만 존재.
   * @param a
   * @param mod
   * @return a의 m에 대한 곱셈 역원
   */
  inline ll multiplicative_inverse(const ll a, const ll mod) {
    ll inverse, gcd;
    tie(inverse, ignore, gcd) = extended_gcd(a, mod);

    if (gcd != 1)
      throw invalid_argument("Multiplicative inverse does not exist");

    // 음수일 수도 있으므로 양수로 변환
    return (inverse % mod + mod) % mod;
  }

  /**
   * 페르마의 소정리 기반 ax ≡ 1 (mod m)일 때의 x의 a의 m에 대한 곱셈 역원 계산. O(log mod).
   * @note mod는 소수, gcd(a, mod) = 1.
   * @param a
   * @param mod
   */
  inline ll fermat_inverse(ll a, const ll mod) {
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
} // namespace math

#endif // MULTIPLICATIVE_INVERSE_HPP
