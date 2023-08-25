#include <bits/stdc++.h>
#include <ranges>

typedef unsigned int uint;
typedef long long int lnt;
using namespace std;

#define len(x) (sizeof(x)/sizeof(x[0]))
#define mod 1000000007
#define endl "\n"

void solve() {
	int n;
	cin >> n;

	deque<pair<int, int>> meetings(n);
	for (auto &p : meetings) cin >> p.first >> p.second;

	ranges::sort(meetings, [](auto p1, auto p2) { return (p1.second == p2.second) ? p1.first < p2.first : p1.second < p2.second; });

	int count = 1;
	int endtime = meetings[0].second;
	for (int i = 1; i < meetings.size(); ++i) {
		if (meetings[i].first < endtime) continue;
		else {
			endtime = meetings[i].second;
			count++;
		}
	}

	cout << count;
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