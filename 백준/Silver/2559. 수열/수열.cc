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

lnt get(lnt* arr, int n) {
	if (n < 0) return 0;
	else return arr[n];
}

void solve() {
	int n, count;
	cin >> n >> count;

	lnt* arr = new lnt[n];
	for (int i = 0; i < n; ++i) {
		cin >> arr[i];
		arr[i] = get(arr, i - 1) + get(arr, i);
	}

	lnt max = numeric_limits<lnt>::min();
	for (int i = 0; i < n - count + 1; ++i) {
		lnt x = get(arr, i + count - 1) - get(arr, i - 1);
		if (max < x) max = x;
	}

	cout << max;
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