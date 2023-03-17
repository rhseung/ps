#include <bits/stdc++.h>
#include <ranges>

typedef unsigned int uint;
typedef long long int lnt;
using namespace std;

#define len(x) (sizeof(x)/sizeof(x[0]))
#define mod 1000000007
#define endl "\n"

void solve() {
	int n, m;
	cin >> n >> m;

	vector<int> v(n + 1);
	iota(v.begin(), v.end(), 0);
	for (int i = 0; i < m; ++i) {
		int a, b;
		cin >> a >> b;
		swap(v[a], v[b]);
	}

	for (int i = 1; i <= n; ++i) {
		cout << v[i] << " ";
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