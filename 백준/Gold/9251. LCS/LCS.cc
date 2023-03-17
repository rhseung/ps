#include <bits/stdc++.h>
#include <ranges>

typedef unsigned int uint;
typedef long long int lnt;
using namespace std;

#define len(x) (sizeof(x)/sizeof(x[0]))
#define mod 1000000007
#define endl "\n"

void solve() {
	string s1, s2;
	cin >> s1 >> s2;

	deque<deque<int>> dp(s1.length(), deque<int>(s2.length(), 0));
	for (int i = 0; i < dp.size(); ++i) {
		for (int j = 0; j < dp[i].size(); ++j) {
			int n1 = (i < 1 or j < 0) ? 0 : dp[i - 1][j];
			int n2 = (i < 0 or j < 1) ? 0 : dp[i][j - 1];
			int n3 = (i < 1 or j < 1) ? 0 : dp[i - 1][j - 1];

			dp[i][j] = (s1[i] == s2[j]) ? n3 + 1 : max(n1, n2);
		}
	}
	cout << dp[s1.length() - 1][s2.length() - 1];

//	# A C A Y K P
//	C 0 1 1 1 1 1
//	A 1 1 2 2 2 2
//	P 1 1 2 2 2 3
//	C 1 2 2 2 2 3
//	A 1 2 3 3 3 3
//	K 1 2 3 3 4 4
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