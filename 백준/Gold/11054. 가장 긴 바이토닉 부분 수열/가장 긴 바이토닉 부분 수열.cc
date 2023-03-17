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

	int* inputs = new int[n];
	for (int i = 0; i < n; ++i) cin >> inputs[i];

	deque<int> dp_up(n, 1);
	deque<int> dp_down(n, 1);

	for (int i = 0; i < n; ++i) {
		for (int j = 0; j < i; ++j) {
			if (inputs[j] < inputs[i]) {
				dp_up[i] = max(dp_up[i], dp_up[j] + 1);
			}
		}
	}

	for (int i = n - 1; i >= 0; --i) {
		for (int j = i + 1; j < n; ++j) {
			if (inputs[i] > inputs[j]) {
				dp_down[i] = max(dp_down[i], dp_down[j] + 1);
			}
		}
	}

	int most = 0;
	for (int i = 0; i < n; ++i) {
		most = max(most, dp_up[i] + dp_down[i] - 1);
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