//
// Created by Hyunseung Ryu on 2025. 7. 21..
//

#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);
  cout.tie(nullptr);

  ll n;
  cin >> n;

  const auto A = new ll[n];
  for (int i = 0; i < n; i++) {
    cin >> A[i];
  }

  ll l = 0, r = n - 1;
  ll min_sum = LLONG_MAX;
  pair<ll, ll> ans = {l, r};

  while (l < r) {
    const ll sum = A[l] + A[r];

    if (abs(min_sum) > abs(sum)) {
      min_sum = sum;
      ans = {l, r};
    }

    if (sum > 0) {
      r--;
    } else if (sum < 0) {
      l++;
    } else {
      break;
    }
  }

  cout << A[ans.first] << " " << A[ans.second] << endl;

  delete[] A;

  return 0;
}