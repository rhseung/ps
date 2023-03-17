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
	string input;

	while (true) {
		getline(cin, input);
		if (input == ".") break;

//		cout << input << ": ";

		stack<char> brackets;
		for (int i = 0; i < input.length() - 1; ++i) {
			if (input[i] == '(' or input[i] == '[')
				brackets.push(input[i]);
			else if (input[i] == ')') {
				if (brackets.empty() or brackets.top() != '(') brackets.push(input[i]);
				else brackets.pop();
			}
			else if (input[i] == ']') {
				if (brackets.empty() or brackets.top() != '[') brackets.push(input[i]);
				else brackets.pop();
			}
		}

		cout << (brackets.empty() ? "yes" : "no") << endl;
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