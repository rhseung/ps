//
// Created by Hyunseung Ryu on 2025. 7. 21..
//

#ifndef LINE_INTERSECT_HPP
#define LINE_INTERSECT_HPP

#include "ccw.hpp"

#include <utility>

#include "vector2d.hpp"

using namespace std;
typedef long long ll;

template <typename T>
using point = pair<T, T>;

template <typename T>
  requires(integral<T> || floating_point<T>)
optional<graph::Vector2d<T>>
find_intersect(const graph::Vector2d<T>& a, const graph::Vector2d<T>& b,
               const graph::Vector2d<T>& c, const graph::Vector2d<T>& d) {
  T det = (b - a).cross(d - c);

  if (det == 0) { // 평행
    if (b == c && a <= c)
      return b;
    else if (a == d && d <= a)
      return a;
    else
      return nullopt;
  }
  else {
    auto p = (c - a).cross(d - c) / det;
    return a + (b - a) * p;
  }
}

namespace graph {
  /**
   * 선분 교차 여부를 확인합니다.
   * @tparam T 선분의 좌표 타입
   * @param line1
   * @param line2
   * @return 선분이 교차하면 true, 그렇지 않으면 false
   */
  template <typename T>
    requires(integral<T> || floating_point<T>)
  bool is_line_intersect(const pair<Vector2d<T>, Vector2d<T>>& line1,
                         const pair<Vector2d<T>, Vector2d<T>>& line2) {
    auto p1 = line1.first, p2 = line1.second, p3 = line2.first, p4 = line2.second;

    T ccw_base_line1 = ccw(p1, p2, p3) * ccw(p1, p2, p4);
    T ccw_base_line2 = ccw(p3, p4, p1) * ccw(p3, p4, p2);

    // 두 선분이 일직선상에 있을 때
    if (ccw_base_line1 == 0 && ccw_base_line2 == 0) {
      if (p1 > p2)
        swap(p1, p2);
      if (p3 > p4)
        swap(p3, p4);

      return p1 <= p4 && p3 <= p2; // 선분이 겹치는지 확인
    }

    return ccw_base_line1 <= 0 && ccw_base_line2 <= 0;
  }

  /**
 * 선분 교차 여부를 확인합니다.
 * @tparam T 선분의 좌표 타입
 * @param L1
 * @param L2
* @return 0: 교점이 없음
1: 교점이 정확히 하나 있으며, 그 교점이 적어도 한 선분의 끝점임
2: 교점이 정확히 하나 있으며, 그 교점이 어느 선분의 끝점도 아님
3: 교점이 무한히 많이 있음
 */
  template <typename T>
  int is_line_intersect_detail(const pair<Vector2d<T>, Vector2d<T>>& L1, const pair<Vector2d<T>, Vector2d<T>>& L2) {
    auto [p1, p2] = L1;
    auto [p3, p4] = L2;

    auto c123 = ccw(p1, p2, p3);
    auto c124 = ccw(p1, p2, p4);
    auto c341 = ccw(p3, p4, p1);
    auto c342 = ccw(p3, p4, p2);

    // 한 선의 두 점이 모두 다른 선의 직선 위에 있는 경우
    if (c123 == 0 && c124 == 0) {
      if (p1 > p2) swap(p1, p2);
      if (p3 > p4) swap(p3, p4);

      if (p2 < p3 || p4 < p1) return 0; // 안 겹침
      if (p2 == p3 || p4 == p1) return 1; // 한 점만 맞닿음
      return 3; // 무한히 겹침
    }

    // 일반 교차 조건
    T s1 = c123 * c124;
    T s2 = c341 * c342;

    if (!(s1 <= 0 && s2 <= 0)) return 0; // 교점 없음
    if (s1 == 0 || s2 == 0) return 1; // 끝점 접촉
    return 2; // 내부 교차
  }


  /**
   * 선분 교차 위치를 찾습니다.
   * @tparam T 선분의 좌표 타입
   * @param line1
   * @param line2
   * @param is_intersect 선분이 교차하는지 여부를 저장할 변수
   * @return 교차점이 존재하면 (무수히 많은 교차점이 존재하는 경우는 제외하고)
   * optional<Vector2d<T>> 타입으로 교차점을 반환합니다.
   */
  template <typename T>
    requires(integral<T> || floating_point<T>)
  optional<Vector2d<T>>
  find_line_intersect(const pair<Vector2d<T>, Vector2d<T>>& line1,
                      const pair<Vector2d<T>, Vector2d<T>>& line2,
                      bool& is_intersect) {
    auto p1 = line1.first, p2 = line1.second, p3 = line2.first, p4 = line2.second;

    T ccw_base_line1 = ccw(p1, p2, p3) * ccw(p1, p2, p4);
    T ccw_base_line2 = ccw(p3, p4, p1) * ccw(p3, p4, p2);

    // 두 선분이 일직선상에 있을 때
    if (ccw_base_line1 == 0 && ccw_base_line2 == 0) {
      if (p1 > p2)
        swap(p1, p2);
      if (p3 > p4)
        swap(p3, p4);

      if (!(p1 <= p4 && p3 <= p2)) // 선분이 겹치지 않는 경우
        return nullopt;

      is_intersect = true;
      return find_intersect<T>(p1, p2, p3, p4);
    }

    if (!(ccw_base_line1 <= 0 &&
      ccw_base_line2 <= 0)) // 선분이 교차하지 않는 경우
      return nullopt;

    is_intersect = true;
    return find_intersect<T>(p1, p2, p3, p4);
  }
} // namespace graph

#endif // LINE_INTERSECT_HPP
