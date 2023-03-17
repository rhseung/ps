#include <bits/stdc++.h>
#include <ranges>

typedef unsigned int uint;
typedef long long int lnt;
using namespace std;

#define mod 1'000'000'000
#define endl "\n"
#define loop(n) for(int _ = 0; _ < n; ++_)
#define loopin(x, start, end) for(int x = start; x <= end; ++x)
#define each(v, arr) for(typeof(v) &v : arr)
#define sum(l, f) ({lnt acc = 0; l{acc += f;} acc;})
#define product(l, f) ({int acc = 1; l{acc *= f;} acc;})
#define lambda(result, ...) [](__VA_ARGS__) { result; }

lnt dp[101][10];

lnt get(int n, int last) {
	if (last < 0 || last > 9) return 0;
	else if (n == 1 and last == 0) return 0;
	else if (n == 1) return 1;
	else if (dp[n][last] != 0) return dp[n][last];

	dp[n][last] = (get(n - 1, last - 1) % mod + get(n - 1, last + 1) % mod) % mod;
	return dp[n][last];
}

void solve() {
	int n;
	cin >> n;

//	loopin(x, 0, 9) cout << n << ", " << x << ": " << get(n, x) << endl;
	cout << (sum(loopin(x, 0, 9), get(n, x) % mod)) % mod;
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