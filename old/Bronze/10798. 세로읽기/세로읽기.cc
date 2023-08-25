#include <bits/stdc++.h>
#include <ranges>

typedef unsigned int uint;
typedef long long int lnt;
using namespace std;

#define len(x) (sizeof(x)/sizeof(x[0]))
#define mod 1000000007
#define endl "\n"

void solve() {
	char str[5][15+1] = {0,};
	for (auto & i : str) cin >> i;

	for (int i = 0; i < 15; ++i) {
		for (int j = 0; j < 5; ++j) {
			if (str[j][i] != 0) cout << str[j][i];
		}
	}
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