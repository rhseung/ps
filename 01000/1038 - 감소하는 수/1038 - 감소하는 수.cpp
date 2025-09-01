#include <bits/stdc++.h>
#define endl "\n"
#define INF 0x3f3f3f3f

using namespace std;
typedef long long int lnt;

void dfs(vector<lnt> &ans, lnt n) {
  // 9876543210이 최대, long long int.
  ans.push_back(n);
  for (int i = 0; i < n % 10; ++i)
    dfs(ans, n * 10 + i);
}

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);
  cout.tie(nullptr);

  int n;
  cin >> n;

  vector<lnt> ans;
  for (int i = 0; i < 10; ++i)
    dfs(ans, i);

  ranges::sort(ans);

  if (n < ans.size())
    cout << ans[n] << endl;
  else
    cout << -1 << endl;

  return 0;
}