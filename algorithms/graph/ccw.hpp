//
// Created by Hyunseung Ryu on 2025. 7. 21..
//

#ifndef CCW_HPP
#define CCW_HPP

#include <utility>

#include "vector2d.hpp"

using namespace std;
typedef long long ll;

namespace graph {
  /**
   * CCW (Counter Clock Wise) - 세 점의 방향을 구합니다.
   * @tparam T 세 점의 좌표 타입
   * @param p1 첫 번째 점
   * @param p2 두 번째 점
   * @param p3 세 번째 점
   * @return <b>0</b>: 세 점이 일직선상에 있을 때, <b>1</b>: p1 -> p2 -> p3가
   * 반시계 방향일 때, <b>-1</b>: 시계 방향일 때
   */
  template <typename T>
    requires(integral<T> || floating_point<T>)
  T ccw(const Vector2d<T>& p1, const Vector2d<T>& p2, const Vector2d<T>& p3) {
    const Vector2d<T> v12 = p2 - p1;
    const Vector2d<T> v23 = p3 - p2;
    const T cross_product = v12.cross(v23);

    return cross_product == 0 ? 0 : (cross_product > 0 ? 1 : -1);
  }
} // namespace graph

#endif // CCW_HPP
