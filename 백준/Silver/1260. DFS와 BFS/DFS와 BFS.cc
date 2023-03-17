#include <bits/stdc++.h>
#include <ranges>

#define mod 1000000007
#define endl "\n"
typedef unsigned int uint;
typedef long long int lnt;
using namespace std;

int num_points, num_lines, start_point;

void dfs(int start, deque<deque<int>> lines, deque<bool> visited) {
	int i = 1;
	stack<int> s;
	visited[start] = true;
	cout << start << " ";

	do {
		bool all = true;
		for (auto n : lines[start]) {
			if (!visited[n]) {
				all = false;
				s.push(start);
				cout << n << " ";

				visited[n] = true;
				start = n;
				break;
			}
		}

		if (all && s.size() > 0) {
			start = s.top();
			s.pop();
		}

		i++;
	} while (!(s.empty() && i >= num_points));
}

void bfs(int start, deque<deque<int>> lines, deque<bool> visited) {
	queue<int> q;
	q.push(start);
	visited[start] = true;

	while (!q.empty()) {
		start = q.front();
		q.pop();
		cout << start << " ";

		for (auto n : lines[start]) {
			if (!visited[n]) {
				q.push(n);
				visited[n] = true;
			}
		}
	}
}

void solve() {
	cin >> num_points >> num_lines >> start_point;

	deque<deque<int>> lines(10000 + 1);
	for (int i = 0; i < num_lines; ++i) {
		int start, end;
		cin >> start >> end;

		lines[start].push_back(end);
		lines[end].push_back(start);

		ranges::sort(lines[start]);
		ranges::sort(lines[end]);
	}

	deque<bool> visited1(num_points + 1, false), visited2(num_points + 1, false);
	dfs(start_point, lines, visited1);
	cout << endl;
	bfs(start_point, lines, visited2);
}

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	// cout << fixed;
	// cout.precision(1);

	// int T; cin >> T; while(T--)
	solve();

	return 0;
}