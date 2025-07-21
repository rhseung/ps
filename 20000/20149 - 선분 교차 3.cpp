//
// Created by Hyunseung Ryu on 2025. 7. 21..
//

#include <bits/stdc++.h>
#define endl "\n"
#define INF 0x3f3f3f3f

using namespace std;
using ll = long long;

template <typename T>
  requires(integral<T> || floating_point<T>)
class Vector2d {
public:
  T x;
  T y;

  explicit Vector2d(const T x, const T y) : x{x}, y{y} {}
  explicit Vector2d(pair<T, T> p) : x{p.first}, y{p.second} {}
  Vector2d(initializer_list<T> list) {
    if (list.size() != 2) {
      throw invalid_argument(
          "Initializer list must contain exactly two elements.");
    }

    auto it = list.begin();
    x = *it++;
    y = *it;
  }
  Vector2d() = default;
  ~Vector2d() = default;

  T cross(const Vector2d<T> &other) const { return x * other.y - y * other.x; }

  T dot(const Vector2d<T> &other) const { return x * other.x + y * other.y; }

  Vector2d operator+(const Vector2d<T> &other) const {
    return {x + other.x, y + other.y};
  }

  Vector2d operator-(const Vector2d<T> &other) const {
    return {x - other.x, y - other.y};
  }

  template <typename U>
    requires(integral<T> || floating_point<T>)
  Vector2d operator*(const U scalar) const {
    return {x * scalar, y * scalar};
  }

  template <typename U>
    requires(integral<T> || floating_point<T>)
  Vector2d operator/(const U scalar) const {
    return {x / scalar, y / scalar};
  }

  Vector2d operator*(const Vector2d<T> &other) const {
    return {x * other.x, y * other.y};
  }

  auto operator<=>(const Vector2d<T> &other) const = default;

  friend istream &operator>>(istream &in, Vector2d<T> &v) {
    return in >> v.x >> v.y;
  }
};

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
T ccw(const Vector2d<T> &p1, const Vector2d<T> &p2, const Vector2d<T> &p3) {
  const Vector2d<T> v12 = p2 - p1;
  const Vector2d<T> v23 = p3 - p2;
  const T cross_product = v12.cross(v23);

  return cross_product == 0 ? 0 : (cross_product > 0 ? 1 : -1);
}

template <typename T>
  requires(integral<T> || floating_point<T>)
optional<Vector2d<T>> find_intersect(const Vector2d<T> &a, const Vector2d<T> &b,
                                     const Vector2d<T> &c,
                                     const Vector2d<T> &d) {
  T det = (b - a).cross(d - c);

  if (det == 0) { // 평행
    if (b == c && a <= c)
      return b;
    else if (a == d && d <= a)
      return a;
    else
      return nullopt;
  } else {
    auto p = (c - a).cross(d - c) / det;
    return a + (b - a) * p;
  }
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
find_line_intersect(const pair<Vector2d<T>, Vector2d<T>> &line1,
                    const pair<Vector2d<T>, Vector2d<T>> &line2,
                    bool &is_intersect) {
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

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);
  cout.tie(nullptr);
  cout << fixed;
  cout.precision(9);

  Vector2d<double> p1, p2, p3, p4;
  cin >> p1 >> p2 >> p3 >> p4;

  bool is_intersect;
  const auto intersection =
      find_line_intersect<double>({p1, p2}, {p3, p4}, is_intersect);

  if (is_intersect) {
    cout << 1 << endl;
    if (intersection.has_value())
      cout << intersection->x << " " << intersection->y << endl;
  } else {
    cout << 0 << endl;
  }

  return 0;
}