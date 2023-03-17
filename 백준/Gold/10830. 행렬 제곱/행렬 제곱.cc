#include <bits/stdc++.h>
#include <ranges>

typedef unsigned int uint;
typedef long long int lnt;
using namespace std;

#define len(x) (sizeof(x)/sizeof(x[0]))
#define mod 1000
#define endl "\n"

using matrix = deque<deque<int>>;

matrix operator*(matrix a, matrix b) {
	int n = a.size();
	matrix ret(n, deque<int>(n));

	for (int i = 0; i < n; ++i) {
		for (int j = 0; j < n; ++j) {
			int sum = 0;
			for (int k = 0; k < n; ++k) {
				sum = (sum + (a[i][k] % mod * b[k][j] % mod) % mod) % mod;
			}
			ret[i][j] = sum;
		}
	}

	return ret;
}

matrix operator^(matrix m, lnt p) {
	if (p == 1) return m;
	else if (p % 2 == 0) return (m * m)^(p / 2);
	else return ((m * m)^(p / 2)) * m;
}

void solve() {
	int n;
	lnt p;
	cin >> n >> p;

	matrix mat(n, deque<int>(n));
	for (int i = 0; i < n; ++i)
		for (int j = 0; j < n; ++j)
			cin >> mat[i][j];

	matrix ret = mat^p;
	for (int i = 0; i < n; ++i) {
		for (int j = 0; j < n; ++j) {
			cout << (ret[i][j] % mod) << " ";
		}
		cout << endl;
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