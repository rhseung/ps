#include <bits/stdc++.h>
#include <ranges>
#define endl "\n"
#define INF 0x3f3f3f3f

using namespace std;

void dfs_recursive(const vector<vector<int>> &adj, const int vtx, unordered_set<int> &visited) {
    visited.insert(vtx);
    cout << vtx << " ";

    for (const int u: adj[vtx]) {
        if (!visited.contains(u)) {
            dfs_recursive(adj, u, visited);
        }
    }
}

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

        for (const int u : ranges::reverse_view(adj[vtx])) {
            if (!visited.contains(u)) {
                stack.push(u);
            }
        }
    }
}

int main() {
    // boj.kr/1260 참고, 대신 vtx는 0부터 시작하는 예제로 변경

    int vertex_count, edge_count, start;
    cin >> vertex_count >> edge_count >> start;

    vector<vector<int>> adj(vertex_count);
    unordered_set<int> visited;

    for (int i = 0; i < edge_count; ++i) {
        int u, v;
        cin >> u >> v;

        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    for (int i = 0; i < vertex_count; ++i) {
        ranges::sort(adj[i]);
    }

    dfs_recursive(adj, start, visited);
    cout << endl;
    dfs(adj, start);

    return 0;
}