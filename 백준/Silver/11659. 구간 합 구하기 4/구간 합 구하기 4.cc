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

int get(int* arr, int n) {
	if (n < 0) return 0;
	else return arr[n];
}

void solve() {
	int n, count;
	cin >> n >> count;

	int* arr = new int[n];
	for (int i = 0; i < n; ++i) {
		int input;
		cin >> input;
		arr[i] = get(arr, i - 1) + input;
	}

	for (int i = 0; i < count; ++i) {
		int s, e;
		cin >> s >> e;
		cout << (get(arr, e-1) - get(arr, s-2)) << endl;
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