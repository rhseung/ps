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
	int cmdcount;
	cin >> cmdcount;

	queue<int> q;
	for (int i = 0; i < cmdcount; ++i) {
		string cmd;
		cin >> cmd;

		if (cmd == "push") {
			int input;
			cin >> input;
			q.push(input);
		}
		else if (cmd == "pop") {
			if (q.empty()) cout << -1 << endl;
			else {
				cout << q.front() << endl;
				q.pop();
			}
		}
		else if (cmd == "size") {
			cout << q.size() << endl;
		}
		else if (cmd == "empty") {
			cout << q.empty() << endl;
		}
		else if (cmd == "front") {
			if (q.empty()) cout << -1 << endl;
			else cout << q.front() << endl;
		}
		else if (cmd == "back") {
			if (q.empty()) cout << -1 << endl;
			else cout << q.back() << endl;
		}
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