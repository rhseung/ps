//
// Created by Hyunseung Ryu on 2025. 7. 19..
//

#ifndef IS_PRIME_HPP
#define IS_PRIME_HPP
#include "mod_operation.hpp"

using ll = long long int;
using ull = unsigned long long int;

// https://github.com/kth-competitive-programming/kactl/blob/main/content/number-theory/MillerRabin.h

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

  /**
   * 확률적 소수 판별 함수, 7*10^18 까지 정확도 보장
   * O(k log n) (k는 테스트 횟수, 일반적으로 7)
   * Miller-Rabin 알고리즘을 사용합니다.
   * @param n
   * @return n이 소수이면 true, 아니면 false
   */
  inline bool is_prime_fast(const ull n) {
    if (n < 2 || n % 6 % 4 != 1) return (n | 1) == 3;
    const ull s = __builtin_ctzll(n - 1);
    const ull d = n >> s;

    for (const ull a : {2, 325, 9375, 28178, 450775, 9780504, 1795265022}) {
      ull p = modpow(a % n, d, n);
      ull i = s;

      while (p != 1 && p != n - 1 && a % n && i--)
        p = modmul(p, p, n);

      if (p != n - 1 && i != s)
        return false;
    }

    return true;
  }
} // namespace math

#endif // IS_PRIME_HPP
