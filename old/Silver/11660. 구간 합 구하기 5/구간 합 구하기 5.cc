#include <bits/stdc++.h>
#include <ranges>

typedef unsigned int uint;
typedef long long int lnt;
using namespace std;

#define len(x) (sizeof(x)/sizeof(x[0]))
//#define mod 1'000'000'000
#define endl "\n"
#define loop(n) for(int _ = 0; _ < n; ++_)
#define loopin(x, start, end) for(int x = start; x <= end; ++x)
#define each(v, arr) for(typeof(v) &v : arr)
#define sum(l, f) ({lnt acc = 0; l{acc += f;} acc;})
#define product(l, f) ({int acc = 1; l{acc *= f;} acc;})
#define lambda(result, ...) [](__VA_ARGS__) { result; }

void solve() {
	int size, count;
	cin >> size >> count;

	int** table = new int*[size];
	for (int i = 0; i < size; ++i) {
		table[i] = new int[size];
		for (int j = 0; j < size; ++j) {
			cin >> table[i][j];
			table[i][j] += (j == 0 ? 0 : table[i][j - 1]);
		}
	}

	for (int i = 0; i < count; ++i) {
		int r1, c1, r2, c2;
		cin >> r1 >> c1 >> r2 >> c2;
		r1--; c1--; r2--; c2--;

		lnt ans = 0;
		for (int r = r1; r <= r2; ++r) {
			ans += table[r][c2] - (c1 == 0 ? 0 : table[r][c1 - 1]);
		}

		cout << ans << endl;
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