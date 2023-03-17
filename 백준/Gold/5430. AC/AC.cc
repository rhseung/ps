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
	string commands;
	cin >> commands;
	queue<char> command;
	for (char &c : commands)
		command.push(c);

	int length;
	cin >> length;
	deque<int> dq;

	string input;
	cin >> input;

	if (input != "[]") {
		int x = 0;
		for (char& ip : input) {
			if (isdigit(ip))
				x = x * 10 + (ip - '0');
			else if (ip == ',' or ip == ']') {
				dq.push_back(x);
				x = 0;
			}
		}
	}

	bool reversed = false;
	while (!command.empty()) {
		switch (command.front()) {
			case 'R':
				reversed = !reversed;
				break;
			case 'D':
				if (dq.empty()) {
					cout << "error" << endl;
					return;
				}
				else {
					if (reversed)
						dq.pop_back();
					else
						dq.pop_front();
				}
				break;
		}
		command.pop();
	}

	if (reversed) ranges::reverse(dq);

	cout << '[';
	for (int i = 0; i < dq.size(); ++i) {
		cout << dq[i] << (i == dq.size() - 1 ? "" : ",");
	}
	cout << ']' << endl;
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