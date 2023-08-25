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
	int n, mod;
	cin >> n >> mod;

	deque<lnt> arr(n), cnt(mod, 0);
	for (int i = 0; i < n; ++i) {
		cin >> arr[i];
		arr[i] = ((i == 0 ? 0 : arr[i - 1]) + arr[i] % mod) % mod;
		cnt[arr[i]]++;
	}

	//	1 0 0 1 0
	//	[3, 2, 0] => 3C2 + 2C2 + 0C2 + 3
	lnt count = cnt[0];
	for (int i = 0; i < mod; ++i) {
		count += cnt[i] * (cnt[i] - 1) / 2;
	}

	cout << count;
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