//
// Created by Hyunseung Ryu on 2025. 7. 21..
//

#ifndef VECTOR2D_HPP
#define VECTOR2D_HPP

#include <concepts>
#include <stdexcept>
#include <utility>

using namespace std;
using ll = long long;

namespace graph {

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

  template <typename U, typename R = decltype(T{} * U{})>
    requires(integral<U> || floating_point<U>)
  [[nodiscard]] R cross(const Vector2d<U> &other) const {
    return x * other.y - y * other.x;
  }

  template <typename U, typename R = decltype(T{} * U{})>
    requires(integral<U> || floating_point<U>)
  [[nodiscard]] R dot(const Vector2d<U> &other) const {
    return x * other.x + y * other.y;
  }

  template <typename U, typename R = decltype(T{} + U{})>
    requires(integral<U> || floating_point<U>)
  Vector2d<R> operator+(const Vector2d<U> &other) const {
    return {x + other.x, y + other.y};
  }

  template <typename U, typename R = decltype(T{} - U{})>
    requires(integral<U> || floating_point<U>)
  Vector2d<R> operator-(const Vector2d<U> &other) const {
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
  Vector2d<R> operator*(const Vector2d<U> &other) const {
    return {x * other.x, y * other.y};
  }

  template <typename U, typename R = decltype(T{} / U{})>
    requires(integral<T> || floating_point<T>)
  Vector2d<R> operator/(const Vector2d<U> &other) const {
    return {x / other.x, y / other.y};
  }

  auto operator<=>(const Vector2d &) const = default;

  friend istream &operator>>(istream &in, Vector2d &v) {
    return in >> v.x >> v.y;
  }

  friend ostream &operator<<(ostream &out, const Vector2d &v) {
    return out << v.x << " " << v.y;
  }
};

} // namespace graph

#endif // VECTOR2D_HPP
