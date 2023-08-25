#include <bits/stdc++.h>
#include <ranges>

typedef unsigned int uint;
typedef long long int lnt;
using namespace std;

#define len(x) (sizeof(x)/sizeof(x[0]))
#define mod 1000000007
#define endl "\n"

deque<int> shift(deque<int> dq, int start, int end) {
	int tmp = dq[start];
	dq.insert(dq.begin() + end + 1, tmp);
	dq.erase(dq.begin() + start);
	return dq;
}

void solve() {
	int n, m;
	cin >> n >> m;

	deque<int> list(n);
	iota(list.begin(), list.end(), 1);
	for (int i = 0; i < m; ++i) {
		int begin, end, mid;
		cin >> begin >> end >> mid;
		for (int j = 0; j < mid - begin; ++j) {
			list = shift(list, begin - 1, end - 1);
		}
	}

	for (int i = 0; i < n; ++i) {
		cout << list[i] << " ";
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