#include <bits/stdc++.h>
#include <ranges>

#define mod 1000000007
#define endl "\n"

typedef unsigned int uint;
typedef long long int lnt;
using namespace std;

int dp[500][500];

int get(int i, int j) {
	if (i < 0 || j < 0) return 0;
	return dp[i][j];
}

void solve() {
	int n, x;
	cin >> n;

	for (int i = 0; i < n; ++i) {
		for (int j = 0; j <= i; ++j) {
			cin >> x;

			dp[i][j] = x + max(get(i - 1, j - 1), get(i - 1, j));
		}
	}

	cout << *max_element(dp[n - 1], dp[n - 1] + n);
}

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	cout << fixed;
	cout.precision(6);

	// size_t T; cin >> T; while(T--)
	solve();

	return 0;
}