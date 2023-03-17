#include <bits/stdc++.h>
#include <ranges>

typedef unsigned int uint;
typedef long long int lnt;
using namespace std;

#define len(x) (sizeof(x)/sizeof(x[0]))
#define mod 1'000'000'007
#define endl "\n"

using matrix = deque<deque<lnt>>;

matrix operator*(matrix a, matrix b) {
	assert(a[0].size() == b.size());

	int l = b.size();
	int n = a.size();
	int m = b[0].size();
	matrix ret(n, deque<lnt>(m));

	for (int i = 0; i < n; ++i) {
		for (int j = 0; j < m; ++j) {
			lnt sum = 0;
			for (int k = 0; k < l; ++k) {
				sum = (sum + (a[i][k] % mod * b[k][j] % mod) % mod) % mod;
			}
			ret[i][j] = sum;
		}
	}

	return ret;
}

matrix operator^(matrix m, lnt p) {
	if (p == 1) return m;
	else if (p % 2 == 0) return (m * m) ^ (p / 2);
	else return ((m * m) ^ (p / 2)) * m;
}

void solve() {
	lnt n;
	cin >> n;

	if (n == 1 or n == 2) cout << 1;
	else {
		matrix coeff = {
			{1, 1},
			{1, 0}
		};
		matrix init = {
			{1},
			{1}
		};

		cout << ((coeff ^ (n - 2)) * init)[0][0];
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