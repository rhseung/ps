//
// Created by Hyunseung Ryu on 2025. 7. 19..
//

#ifndef FAST_POWER_HPP
#define FAST_POWER_HPP

using namespace std;
typedef long long ll;

namespace math {

/**
 * 빠른 거듭제곱
 * @param base
 * @param exp
 * @param mod
 * @return
 */
inline ll fast_power(const ll base, const ll exp, const ll mod) {
  if (exp == 0)
    return 1;
  if (exp == 1)
    return base % mod;

  const ll half = fast_power(base, exp / 2, mod);
  return (half * half % mod) * fast_power(base, exp - 2 * (exp / 2), mod) % mod;
}

} // namespace math

#endif // FAST_POWER_HPP
