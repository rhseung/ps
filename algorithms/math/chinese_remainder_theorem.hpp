//
// Created by Hyunseung Ryu on 2025. 7. 19..
//

#ifndef CHINESE_REMAINDER_THEOREM_HPP
#define CHINESE_REMAINDER_THEOREM_HPP

#include "multiplicative_inverse.hpp"

#include <assert.h>
#include <vector>

using namespace std;
typedef long long ll;

namespace math {

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
inline ll chinese_remainder_theorem(const vector<ll> &a, const vector<ll> &m) {
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

} // namespace math

#endif // CHINESE_REMAINDER_THEOREM_HPP
