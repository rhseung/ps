//
// Created by Hyunseung Ryu on 2025. 7. 23..
//

#ifndef LIS_HPP
#define LIS_HPP

#include <functional>
#include <vector>

namespace search {
  /**
   * LIS, 가장 긴 증가 부분 수열의 길이를 구하는 함수
   * @param A 입력 배열, 가장 긴 증가 부분 수열을 찾을 대상
   * @return 가장 긴 증가 부분 수열의 길이
   * @note O(NlogN) 시간 복잡도
   */
  inline std::size_t length_LIS(const std::vector<int>& A) {
    std::vector<int> D; // LIS 끝 값 추적, D[i] = 길이 i인 증가 수열 중 마지막
    // 원소가 최소가 되는 경우의 그 끝 값

    for (int a : A) {
      auto it = std::ranges::lower_bound(D, a);

      if (it == D.end()) {
        D.push_back(a);
      }
      else {
        *it = a; // D[it - D.begin()] = a;
      }
    }

    return D.size();
  }

  /**
   * LIS, 가장 긴 증가 부분 수열을 직접 역추적하여 찾는 함수
   * @param A 입력 배열, 가장 긴 증가 부분 수열을 찾을 대상
   * @param proj 프로젝션 함수, A[i]를 어떤 값으로 변환하여 비교할지 결정하는 함수
   * @return 가장 긴 증가 부분 수열
   * @note O(NlogN) 시간 복잡도
   */
  template <typename T, typename Proj = std::identity>
  std::vector<T>
  find_LIS(const std::vector<T>& A, const Proj& proj = [](T t) {
             return t;
           }) {
    const std::size_t n = A.size();

  // clang-format off
  std::vector<T> D;        // LIS 끝 값 추적, D[i] = 길이 i인 증가 수열 중 마지막 원소가 최소가 되는 경우의 그 끝 값
  std::vector<int> D_idx;    // A[D_idx[i]] = D[i] (i번째 LIS 끝 값), D_idx[i]는 D[i]가 A의 몇 번째 원소인지 추적
  std::vector<int> P(n);     // A[i] 이전의 LIS 원소 인덱스, A[i] -> A[P[i]] -> A[P[P[i]]] ...로 수열 거꾸로 복원
    // clang-format on

    for (int i = 0; i < n; ++i) {
      auto it = std::ranges::lower_bound(D, proj(A[i]), std::less{}, proj);
      const auto it_idx = it - D.begin();

      if (it_idx >= D.size()) {
        D.push_back(A[i]);
        D_idx.push_back(i);
      }
      else {
        D[it_idx] = A[i];
        D_idx[it_idx] = i;
      }

      if (it_idx > 0) {
        P[i] = D_idx[it_idx - 1]; // A[i] 이전의 LIS 원소 인덱스, D[it_idx - 1]가
        // A의 몇 번째 원소인지 찾음
      }
      else {
        P[i] = -1; // A[i]가 LIS의 첫 번째 원소인 경우
      }
    }

  // clang-format off
  std::vector<T> LIS;   // LIS의 마지막 원소는 D.back()
  int idx = D_idx.back(); // D의 마지막 원소가 A의 몇 번째 원소인지, A[idx] = D.back()
    // clang-format on

    while (idx != -1) {
      LIS.push_back(A[idx]); // A[D_idx[i]] = D[i]
      idx = P[idx];
    }

    std::ranges::reverse(LIS);

    return LIS;
  }
} // namespace search

#endif // LIS_HPP
