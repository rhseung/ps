//
// Created by Hyunseung Ryu on 2025. 7. 19..
//

#ifndef IS_PRIME_HPP
#define IS_PRIME_HPP

typedef long long ll;

namespace math {

/**
 * 소수 판별 함수 O(sqrt(n))
 * @param n 판별할 정수
 * @return n이 소수이면 true, 아니면 false
 */
inline bool is_prime(const ll n) {
  if (n < 2)
    return false;
  if (n == 2 || n == 3)
    return true;
  if (n % 2 == 0)
    return false;

  for (ll i = 3; i * i <= n; i += 2) {
    if (n % i == 0)
      return false;
  }

  return true;
}

} // namespace math

#endif // IS_PRIME_HPP
