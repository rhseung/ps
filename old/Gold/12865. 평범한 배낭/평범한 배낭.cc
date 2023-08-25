#include <bits/stdc++.h>
#include <ranges>

typedef unsigned int uint;
typedef long long int lnt;
using namespace std;

#define len(x) (sizeof(x)/sizeof(x[0]))
#define mod 1'000'000'007
#define endl "\n"
#define loop(n) for(int _ = 0; _ < n; ++_)
#define loopin(x, start, end) for(int x = start; x <= end; ++x)
#define each(v, arr) for(typeof(v) &v : arr)
#define sum(l, f) ({lnt acc = 0; l{acc += f;} acc;})
#define product(l, f) ({int acc = 1; l{acc *= f;} acc;})
#define lambda(result, ...) [](__VA_ARGS__) { result; }

struct item {
	int weight;
	int value;
};

#define max_count 100
#define max_weight 100000
int dp[max_count][max_weight + 1];
item items[max_count];

int dp_get(int i, int j) {
	if (i < 0 or j < 0) return 0;
	else if (dp[i][j] != 0) return dp[i][j];

	int tmp1 = dp_get(i - 1, j);
	int tmp2 = j >= items[i].weight ? dp_get(i - 1, j - items[i].weight) + items[i].value : 0;
	dp[i][j] = max(tmp1, tmp2);
	return dp[i][j];
}

void solve() {
	int count, weight;
	cin >> count >> weight;

	loopin(i, 0, count - 1)
		cin >> items[i].weight >> items[i].value;

	cout << dp_get(count - 1, weight);
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