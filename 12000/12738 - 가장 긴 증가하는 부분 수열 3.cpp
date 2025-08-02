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

  const auto A = new int[n];
  for (int i = 0; i < n; ++i)
    cin >> A[i];

  // D[i] = 길이 i인 증가 수열 중 마지막 원소가 최소가 되는 경우의 그 끝 값
  // => LIS 길이 = D의 길이
  vector<int> D;

  for (int i = 0; i < n; ++i) {
    auto ptr = ranges::lower_bound(D, A[i]);
    // how to get idx: ptr - D.begin()

    if (ptr == D.end()) {
      D.push_back(A[i]);
    } else {
      *ptr = A[i];
    }
  }

  cout << D.size();

  delete[] A;

  return 0;
}
