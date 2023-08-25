#include <bits/stdc++.h>
#include <ranges>

typedef unsigned int uint;
typedef long long int lnt;
using namespace std;

#define len(x) (sizeof(x)/sizeof(x[0]))
#define mod 1000000007
#define endl "\n"

bool is_reverse_same(string s) {
	for (int i = 0; i < s.length(); ++i) {
		if (s[i] != s[s.length() - 1 - i]) return false;
	}
	return true;
}

void solve() {
	string s;
	cin >> s;
	cout << is_reverse_same(s);
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