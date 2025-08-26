//
// Created by Hyunseung Ryu on 2025. 7. 19..
//

#ifndef BINOMIAL_COEFF_HPP
#define BINOMIAL_COEFF_HPP

#include "fast_power.hpp"
#include "radix_convert.hpp"
#include <vector>

#include "mod_operation.hpp"

using namespace std;
typedef long long ll;

namespace math {
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
} // namespace math

#endif // BINOMIAL_COEFF_HPP
