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

	int* times = new int[n];
	for (int i = 0; i < n; ++i) cin >> times[i];

	sort(times, times + n);

	int result = 0;
	for (int i = 0; i < n; ++i) {
		result += times[i] * (n - i);
	}

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