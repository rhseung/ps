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
 * ax + my = 1 => ax ≡ 1 (mod m) => x는 a의 m에 대한 곱셈 역원
 * @param a
 * @param mod
 * @param fallback 곱셈 역원이 존재하지 않을 때 호출되는 함수
 * @return a의 m에 대한 곱셈 역원, gcd(a, m) = 1일 때 존재
 */
inline ll multiplicative_inverse(
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

} // namespace math

#endif // MULTIPLICATIVE_INVERSE_HPP
