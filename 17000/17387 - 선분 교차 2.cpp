//
// Created by Hyunseung Ryu on 2025. 7. 21..
//

#include <bits/stdc++.h>
#define endl "\n"
#define INF 0x3f3f3f3f
#define x first
#define y second

using namespace std;
using ll = long long;

template <typename T> using point = pair<T, T>;

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
  requires integral<T>
T ccw(const point<T> &p1, const point<T> &p2, const point<T> &p3) {
  const point vector_12 = {p2.x - p1.x, p2.y - p1.y};
  const point vector_23 = {p3.x - p2.x, p3.y - p2.y};
  const T cross_product = vector_12.x * vector_23.y - vector_12.y * vector_23.x;

  return cross_product == 0 ? 0 : (cross_product > 0 ? 1 : -1);
}

/**
 * 선분 교차 여부를 확인합니다.
 * @tparam T 선분의 좌표 타입
 * @param line1
 * @param line2
 * @return 선분이 교차하면 true, 그렇지 않으면 false
 */
template <typename T>
  requires integral<T>
bool line_intersect(const pair<point<T>, point<T>> &line1,
                    const pair<point<T>, point<T>> &line2) {
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

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);
  cout.tie(nullptr);

  ll x1, y1, x2, y2, x3, y3, x4, y4;
  cin >> x1 >> y1 >> x2 >> y2 >> x3 >> y3 >> x4 >> y4;
  cout << line_intersect<ll>({{x1, y1}, {x2, y2}}, {{x3, y3}, {x4, y4}})
       << endl;

  return 0;
}