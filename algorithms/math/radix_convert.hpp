//
// Created by Hyunseung Ryu on 2025. 7. 19..
//

#ifndef RADIX_CONVERT_HPP
#define RADIX_CONVERT_HPP

#include <vector>

using namespace std;
typedef long long ll;

namespace math {
  /**
   * n을 radix 진법으로 변환하여 각 자리수를 반환하는 함수.
   * @param number 변환할 숫자
   * @param radix 변환할 진법
   * @returns 각 자리수를 담은 벡터 - 주의: 뒤집혀서 저장됨.
   */
  inline vector<ll> radix_convert(ll number, const ll radix) {
    vector<ll> digits;
    while (number > 0) {
      digits.push_back(number % radix);
      number /= radix;
    }
    return digits;
  }
} // namespace math

#endif // RADIX_CONVERT_HPP
