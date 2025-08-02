//
// Created by Hyunseung Ryu on 2025. 7. 23..
//

#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;

/**
 * 인덱스를 반환하도록 약간 변형함
 * LIS, 가장 긴 증가 부분 수열을 직접 역추적하여 찾는 함수
 * @param A 입력 배열, 가장 긴 증가 부분 수열을 찾을 대상
 * @param proj 프로젝션 함수, A[i]를 어떤 값으로 변환하여 비교할지 결정하는 함수
 * @return 가장 긴 증가 부분 수열의 인덱스들
 * @note O(NlogN) 시간 복잡도
 */
template <typename T, typename Proj = std::identity>
std::vector<int>
find_LIS(const std::vector<T> &A, const Proj &proj = [](T t) { return t; }) {
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
    } else {
      D[it_idx] = A[i];
      D_idx[it_idx] = i;
    }

    if (it_idx > 0) {
      P[i] = D_idx[it_idx - 1]; // A[i] 이전의 LIS 원소 인덱스, D[it_idx - 1]가
      // A의 몇 번째 원소인지 찾음
    } else {
      P[i] = -1; // A[i]가 LIS의 첫 번째 원소인 경우
    }
  }

  // clang-format off
  std::vector<int> LIS_idx;
  int idx = D_idx.back(); // D의 마지막 원소가 A의 몇 번째 원소인지, A[idx] = D.back()
  // clang-format on

  while (idx != -1) {
    LIS_idx.push_back(idx);
    idx = P[idx];
  }

  std::ranges::reverse(LIS_idx);

  return LIS_idx;
}

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);
  cout.tie(nullptr);

  int n;
  cin >> n;

  vector<pair<int, int>> A(n);
  for (auto &p : A) {
    cin >> p.first >> p.second;
  }

  ranges::sort(A);
  const auto LIS_idx =
      find_LIS(A, [](const pair<int, int> &a) { return a.second; });

  vector<bool> removed(n, false);
  for (const auto &idx : LIS_idx) {
    removed[idx] = true;
  }

  cout << n - LIS_idx.size() << endl;
  for (int i = 0; i < n; i++) {
    if (!removed[i]) {
      cout << A[i].first << endl;
    }
  }

  return 0;
}