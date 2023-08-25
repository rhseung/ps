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
	while (true) {
		cin >> n;
		if (n == -1) break;

		string s = " = ";
		int sum = 0;
		for (int i = 1; i < n; ++i) {
			if (n % i == 0) {
				sum += i;
				s += to_string(i) + " + ";
			}
		}

		if (sum == n) cout << n << s.substr(0, s.length() - 3) << endl;
		else cout << n << " is NOT perfect." << endl;
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