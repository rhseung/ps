#include <bits/stdc++.h>
#include <ranges>

typedef unsigned int uint;
typedef long long int lnt;
using namespace std;

#define len(x) (sizeof(x)/sizeof(x[0]))
#define mod 1000000007
#define endl "\n"

void solve() {
	int n;
	cin >> n;

	vector<int> input(n);
	for (auto &i : input) cin >> i;

	vector<int> dp(input.size(), 1);
	for (int i = 0; i < dp.size(); ++i) {
		for (int j = 0; j < i; ++j) {
			if (input[j] < input[i]) {
				dp[i] = max(dp[i], dp[j] + 1);
			}
		}
	}

	int most = 0;
	for (auto i : dp) {
		if (most < i) most = i;
	}
	cout << most;
}

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	cout << fixed;
	cout.precision(6);

	//	size_t T; cin >> T; while (T--)
	solve();

	return 0;
}