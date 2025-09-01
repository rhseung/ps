//
// Created by Hyunseung Ryu on 2025. 8. 2..
//

#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;

/**
 * 2차원 좌표를 나타내는 클래스
 * @tparam T 좌표의 타입
 */
template <typename T>
  requires(integral<T> || floating_point<T>)
class Vector2d {
public:
  T x;
  T y;

  explicit Vector2d(const T x, const T y) : x{x}, y{y} {
  }

  explicit Vector2d(pair<T, T> p) : x{p.first}, y{p.second} {
  }

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

  template <typename U, typename R = decltype(T{} * U{})>
    requires(integral<U> || floating_point<U>)
  [[nodiscard]] R cross(const Vector2d<U>& other) const {
    return x * other.y - y * other.x;
  }

  template <typename U, typename R = decltype(T{} * U{})>
    requires(integral<U> || floating_point<U>)
  [[nodiscard]] R dot(const Vector2d<U>& other) const {
    return x * other.x + y * other.y;
  }

  template <typename U, typename R = decltype(T{} + U{})>
    requires(integral<U> || floating_point<U>)
  Vector2d<R> operator+(const Vector2d<U>& other) const {
    return {x + other.x, y + other.y};
  }

  template <typename U, typename R = decltype(T{} - U{})>
    requires(integral<U> || floating_point<U>)
  Vector2d<R> operator-(const Vector2d<U>& other) const {
    return {x - other.x, y - other.y};
  }

  template <typename U, typename R = decltype(T{} * U{})>
    requires(integral<U> || floating_point<U>)
  Vector2d<R> operator*(const U scalar) const {
    return {x * scalar, y * scalar};
  }

  template <typename U, typename R = decltype(T{} / U{})>
    requires(integral<T> || floating_point<T>)
  Vector2d<R> operator/(const U scalar) const {
    return {x / scalar, y / scalar};
  }

  template <typename U, typename R = decltype(T{} * U{})>
    requires(integral<T> || floating_point<T>)
  Vector2d<R> operator*(const Vector2d<U>& other) const {
    return {x * other.x, y * other.y};
  }

  template <typename U, typename R = decltype(T{} / U{})>
    requires(integral<T> || floating_point<T>)
  Vector2d<R> operator/(const Vector2d<U>& other) const {
    return {x / other.x, y / other.y};
  }

  auto operator<=>(const Vector2d&) const = default;

  friend istream& operator>>(istream& in, Vector2d& v) {
    return in >> v.x >> v.y;
  }

  friend ostream& operator<<(ostream& out, const Vector2d& v) {
    return out << v.x << " " << v.y;
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
T ccw(const Vector2d<T>& p1, const Vector2d<T>& p2, const Vector2d<T>& p3) {
  const Vector2d<T> v12 = p2 - p1;
  const Vector2d<T> v23 = p3 - p2;
  const T cross_product = v12.cross(v23);

  return cross_product == 0 ? 0 : (cross_product > 0 ? 1 : -1);
}

/**
 * @note 리턴에서 ccw_base_line1 <= 0 && ccw_base_line2 <= 0에서 등호를 제외하도록 수정함
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

  return ccw_base_line1 < 0 && ccw_base_line2 < 0;
}

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);
  cout.tie(nullptr);

  Vector2d<int> p1, p2, p3, p4;
  cin >> p1 >> p2 >> p3 >> p4;

  const bool a = is_line_intersect<int>({p1, p2}, {p3, p4});

  cout << a << endl;

  return 0;
}
