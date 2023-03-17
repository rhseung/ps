#include <bits/stdc++.h>
#include <ranges>

typedef unsigned int uint;
typedef long long int lnt;
using namespace std;

#define len(x) (sizeof(x)/sizeof(x[0]))
#define mod 1000000007
#define endl "\n"

void solve() {
	string s;
	cin >> s;

	int n = 0;
	int result = 0;
	bool negative = false;
	for (auto c : s) {
		if (c == '-' or c == '+') {
			result += (-1 * ((negative) ? 1 : -1)) * n;
			if (!negative and c == '-') negative = true;
			n = 0;
		}
		else {
			n = (n * 10) + (c - '0');
		}
	}
	result += (-1 * ((negative) ? 1 : -1)) * n;

	cout << result;
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