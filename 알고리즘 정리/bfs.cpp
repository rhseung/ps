#include <bits/stdc++.h>

#include <ranges>
#define endl "\n"
#define INF 0x3f3f3f3f

using namespace std;

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

        for (const int u : adj[vtx]) {
            if (!visited.contains(u)) {
                queue.push(u);
            }
        }
    }
}

int main() {
    // boj.kr/1260 참고, 대신 vtx는 0부터 시작하는 예제로 변경

    int vertex_count, edge_count, start;
    cin >> vertex_count >> edge_count >> start;

    vector<vector<int>> adj(vertex_count);
    set<int> visited;

    for (int i = 0; i < edge_count; ++i) {
        int u, v;
        cin >> u >> v;

        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    // 정렬을 하는게 중요하네
    for (int i = 0; i < vertex_count; ++i) {
        ranges::sort(adj[i]);
    }

    bfs(adj, start);

    return 0;
}