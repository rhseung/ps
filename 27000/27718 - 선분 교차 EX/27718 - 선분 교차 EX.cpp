// BOJ 27718 - 선분 교차 EX
#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

int res[2000][2000];

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
template <typename T> requires integral<T> || floating_point<T>
T ccw(const Vector2d<T>& p1, const Vector2d<T>& p2, const Vector2d<T>& p3) {
  const Vector2d<T> v12 = p2 - p1;
  const Vector2d<T> v23 = p3 - p2;
  const T cross_product = v12.cross(v23);

  return cross_product == 0 ? 0 : (cross_product > 0 ? 1 : -1);
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
int is_line_intersect(const pair<Vector2d<T>, Vector2d<T>>& L1, const pair<Vector2d<T>, Vector2d<T>>& L2) {
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

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);
  cout.tie(nullptr);

  int n;
  cin >> n;

  vector<pair<Vector2d<ll>, Vector2d<ll>>> lines(n);
  for (int i = 0; i < n; ++i) {
    cin >> lines[i].first >> lines[i].second;
  }

  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < n; ++j) {
      if (i == j) res[i][j] = 3;
      if (i > j) res[i][j] = res[j][i];
      else res[i][j] = is_line_intersect(lines[i], lines[j]);
    }
  }

  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < n; ++j) {
      cout << res[i][j];
    }
    cout << endl;
  }

  return 0;
}
