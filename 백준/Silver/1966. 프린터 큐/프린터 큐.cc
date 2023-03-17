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

struct doc {
	int prior;
	int idx;

	bool operator<(const doc& d) const {
		return prior < d.prior or idx < d.idx;
	}
};

void solve() {
	int doccount, wonder;
	cin >> doccount >> wonder;

	deque<doc> dq;
	for (int i = 0; i < doccount; ++i) {
		int prior;
		cin >> prior;
		dq.push_back(doc{prior, i});
	}

	int popcount = 1;
	while (!dq.empty()) {
		bool flag = true;
		for (int i = 1; i < dq.size(); ++i) {
			if (dq[i].prior > dq.front().prior) {
				flag = false;
				doc tmp = dq.front();
				dq.pop_front();
				dq.push_back(tmp);
			}
		}
		if (flag) {
			if (dq.front().idx == wonder) {
				cout << popcount << endl;
			}
			dq.pop_front();
			popcount++;
		}
	}
}

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	cout << fixed;
	cout.precision(6);

	 size_t T; cin >> T; while(T--)
	solve();

	return 0;
}