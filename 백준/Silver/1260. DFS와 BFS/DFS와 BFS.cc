#include <bits/stdc++.h>
#include <ranges>
#define endl "\n"
#define INF 0x3f3f3f3f

using namespace std;

void dfs(const vector<vector<int>> &adj, const int start) {
    stack<int> stack;
    unordered_set<int> visited;

    stack.push(start);

    while (!stack.empty()) {
        const int vtx = stack.top();
        stack.pop();

        if (visited.contains(vtx)) continue;
        visited.insert(vtx);
        cout << vtx << " ";

        for (auto u : ranges::reverse_view(adj[vtx])) {
            if (!visited.contains(u)) {
                stack.push(u);
            }
        }
    }
}

void bfs(const vector<vector<int>> &adj, const int start) {
    queue<int> queue;
    unordered_set<int> visited;

    queue.push(start);

    while (!queue.empty()) {
        const int vtx = queue.front();
        queue.pop();

        if (visited.contains(vtx)) continue;
        visited.insert(vtx);
        cout << vtx << " ";

        for (auto u : adj[vtx]) {
            if (!visited.contains(u)) {
                queue.push(u);
            }
        }
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n, m, v;
    cin >> n >> m >> v;

    vector<vector<int>> adj(n + 1);

    for (int i = 0; i < m; ++i) {
        int a, b;
        cin >> a >> b;

        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    for (int i = 1; i < adj.size(); ++i) {
        ranges::sort(adj[i]);
    }

    dfs(adj, v);
    cout << endl;
    bfs(adj, v);

    return 0;
}