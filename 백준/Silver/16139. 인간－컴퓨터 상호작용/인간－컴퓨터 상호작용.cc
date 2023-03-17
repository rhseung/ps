#include <bits/stdc++.h>
#include <ranges>

typedef unsigned int uint;
typedef long long int lnt;
using namespace std;

#define len(x) (sizeof(x)/sizeof(x[0]))
#define mod 1'000'000'000
#define endl "\n"
#define loop(n) for(int _ = 0; _ < n; ++_)
#define loopin(x, start, end) for(int x = start; x <= end; ++x)
#define each(v, arr) for(typeof(v) &v : arr)
#define sum(l, f) ({lnt acc = 0; l{acc += f;} acc;})
#define product(l, f) ({int acc = 1; l{acc *= f;} acc;})
#define lambda(result, ...) [](__VA_ARGS__) { result; }

int acc[200001][26];

int get(int i, int j) {
	if (i < 0 or i > 200000) return 0;
	else if (j < 0 or j > 25) return 0;
	else return acc[i][j];
}

void solve() {
	std::string str;
	cin >> str;

	for (int i = 0; i < str.length(); ++i) {
		for (int j = 0; j < 26; ++j) {
			acc[i][j] += (get(i - 1, j) + (j == str[i] - 'a'));
		}
	}

	int q;
	cin >> q;

	for (int i = 0; i < q; ++i) {
		char c;
		int s, e;
		cin >> c >> s >> e;
		cout << (get(e, c - 'a') - get(s - 1, c - 'a')) << endl;
	}
}

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	cout << fixed;
	cout.precision(6);

	// size_t T; cin >> T; while(T--)
	solve();

	return 0;
}