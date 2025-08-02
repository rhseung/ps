#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
typedef long long ll;

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);
  cout.tie(nullptr);

  int n;
  cin >> n;

  vector<int> A(n);
  for (auto &a : A)
    cin >> a;

  // clang-format off
  vector<int> D;        // LIS 끝 값 추적, D[i] = 길이 i인 증가 수열 중 마지막 원소가 최소가 되는 경우의 그 끝 값
  vector<int> D_idx;    // A[D_idx[i]] = D[i] (i번째 LIS 끝 값), D_idx[i]는 D[i]가 A의 몇 번째 원소인지 추적
  vector<int> P(n); // A[i] 이전의 LIS 원소 인덱스, A[i] -> A[P[i]] -> A[P[P[i]]] ...로 수열 거꾸로 복원
  // clang-format on

  for (int i = 0; i < n; ++i) {
    auto it = ranges::lower_bound(D, A[i]);
    auto it_idx = it - D.begin();

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

  vector<int> LIS; // LIS의 마지막 원소는 D.back()
  int idx =
      D_idx.back(); // D의 마지막 원소가 A의 몇 번째 원소인지, A[idx] = D.back()
  while (idx != -1) {
    LIS.push_back(A[idx]); // A[D_idx[i]] = D[i]
    idx = P[idx];
  }

  ranges::reverse(LIS);

  cout << D.size() << endl;
  for (const auto &v : LIS) {
    cout << v << " ";
  }

  return 0;
}
