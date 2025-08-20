// BOJ 9466 - 텀 프로젝트
#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

void dfs(const vector<vector<int>>& graph, vector<bool>& visited, const int now, const int start) {
    visited[now] = true;

    for (const auto neighbor : graph[now]) {
        if (!visited[neighbor])
            dfs(graph, visited, neighbor);
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int n;
        cin >> n;

        vector<vector<int>> graph(n + 1);
        for (int i = 1; i <= n; ++i) {
            int tmp;
            cin >> tmp;

            graph[i].push_back(tmp);
        }
    }

    return 0;
}
