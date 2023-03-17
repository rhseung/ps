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

	deque<int> dq(size);
	iota(dq.begin(), dq.end(), 1);

	int ans = 0, find;
	while (count--) {
		cin >> find;

		int idx;
		for (int i = 0; i < size; ++i) {
			if (find == dq[i]) {
				idx = i;
				break;
			}
		}
		int value = dq[idx];

		if (idx <= dq.size() / 2) {
			while (dq.front() != value) {
				int tmp = dq.front();
				dq.pop_front();
				dq.push_back(tmp);
				ans++; // 2번
			}
		}
		else {
			while (dq.front() != value) {
				int tmp = dq.back();
				dq.pop_back();
				dq.push_front(tmp);
				ans++; // 3번
			}
		}

		dq.pop_front();
		// 1번
	}

	cout << ans;
}

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	cout << fixed;
	cout.precision(6);

//	 size_t T; cin >> T; while(T--)
	solve();

	return 0;
}