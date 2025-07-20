#include <bits/stdc++.h>
#define endl "\n"
#define INF 0x3f3f3f3f

using namespace std;
typedef long long ll;

/**
 * 너비 우선 탐색 (BFS)
 * @param adj 인접 리스트, [시작 정점: [...끝 정점들], ...] 형태.
 * @param start 시작 정점
 * @param visit 방문한 정점을 처리하는 함수, 기본적으로 정점을 출력합니다.
 * @note 끝 정점들은 정렬되어 있어야 합니다.
 */
inline void bfs(const vector<vector<int>> &adj, const int start,
                const function<void(int)> &visit = [](const int v) { cout << v << " "; }) {
    queue<int> queue;
    unordered_set<int> visited;

    queue.push(start);

    while (!queue.empty()) {
        const int vtx = queue.front();
        queue.pop();

        if (visited.contains(vtx))
            continue;
        visited.insert(vtx);

        // 방문한 정점 출력
        visit(vtx);

        // 인접한 정점들을 순회, 정렬되어 있어야 함.
        for (const int u : adj[vtx]) {
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

    int n, e, s;
    cin >> n >> e >> s;

    vector<vector<int>> adj(n + 1);

    for (int i = 0; i < e; ++i) {
        int u, v;
        cin >> u >> v;

        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    for (auto &i : adj) {
        ranges::sort(i, greater());
    }

    int cnt = 1;
    vector<int> order(n + 1, 0);

    bfs(adj, s, [&](const int v) {
        order[v] = cnt++;
    });

    for (int i = 1; i <= n; ++i) {
        cout << order[i] << endl;
    }

    return 0;
}