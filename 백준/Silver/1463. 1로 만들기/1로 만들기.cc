#include <bits/stdc++.h>
#include <ranges>

#define mod 1000000007
#define endl "\n"

typedef unsigned int uint;
typedef long long int lnt;
using namespace std;

int dp[1000001];

int get(int n) {
	if (n == 1) return 0;
	if (dp[n] != 0) return dp[n];

	dp[n] = get(n - 1) + 1;
	if (n % 3 == 0) dp[n] = min(dp[n], get(n / 3) + 1);
	if (n % 2 == 0) dp[n] = min(dp[n], get(n / 2) + 1);
	return dp[n];
}

void solve() {
	int n;
	cin >> n;
	dp[0] = 0;
	dp[1] = 0;
	dp[2] = 1;
	dp[3] = 1;
	cout << get(n);
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