#include <bits/stdc++.h>
#include <ranges>

typedef unsigned int uint;
typedef long long int lnt;
using namespace std;

#define len(x) (sizeof(x)/sizeof(x[0]))
#define mod 1000000007
#define endl "\n"

void solve() {
	int n, k;
	cin >> n >> k;

	deque<int> kinds(n);
	for (int i = 0; i < n; ++i) cin >> kinds[i];

	int count = 0;
	for (auto kind = kinds.rbegin(); kind < kinds.rend(); ++kind) {
		if (*kind > k) continue;

		count += (k / *kind);
		k %= *kind;

		if (*kind == 0) break;
	}

	cout << count;
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