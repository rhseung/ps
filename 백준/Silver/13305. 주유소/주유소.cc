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

	int* length = new int[n - 1];
	for (int i = 0; i < n - 1; ++i) cin >> length[i];

	int* prices = new int[n];
	for (int i = 0; i < n; ++i) cin >> prices[i];

	int min = prices[0];
	lnt amount = 0;
	for (int i = 0; i < n - 1; ++i) {
		if (prices[i] < min)
			min = prices[i];

		amount += length[i] * min;
	}

	cout << amount;
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