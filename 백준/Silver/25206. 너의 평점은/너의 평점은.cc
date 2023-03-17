#include <bits/stdc++.h>
#include <ranges>

typedef unsigned int uint;
typedef long long int lnt;
using namespace std;

#define len(x) (sizeof(x)/sizeof(x[0]))
#define mod 1000000007
#define endl "\n"

void solve() {
	string subject;
	double times;
	string symbol;

	double result = 0.0;
	double whole_times = 0;
	for (int i = 0; i < 20; ++i) {
		cin >> subject >> times >> symbol;
		double score = 0.0;

		if (symbol == "P") continue;
		else if (symbol.length() > 1) {
			score += 4.0 - (symbol[0] - 'A');
			score += (symbol[1] == '+') ? 0.5 : 0.0;
		}

		result += (score * times);
		whole_times += times;
	}

	cout << (result / whole_times);
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