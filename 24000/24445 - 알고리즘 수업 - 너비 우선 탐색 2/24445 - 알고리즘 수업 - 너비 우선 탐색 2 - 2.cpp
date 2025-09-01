#include <bits/stdc++.h>
#define endl "\n"
#define INF 0x3f3f3f3f

using namespace std;
typedef long long ll;

/**
 * 너비 우선 탐색 (BFS) - 인접 행렬
 * @param adj 인접 행렬, adj[i][j]가 true이면 i와 j가 연결되어 있음을 나타냅니다.
 * @param start 시작 정점
 * @param visit 방문한 정점을 처리하는 함수, 기본적으로 정점을 출력합니다.
 * @param reverse 인접 행렬을 역순으로 탐색할지 여부. true이면 인접한 정점들을 역순으로 탐색합니다.
 * @note 정점 번호 오름차순(reverse가 true면 내림차순)으로 방문합니다. 또한 정점 번호는 0부터 시작해야 합니다.
 */
template <typename T> requires integral<T>
void bfs_matrix(const vector<vector<bool>> &adj, const T start,
                const function<void(T)> &visit = [](const T v) { cout << v << " "; }, const bool reverse = false) {
    assert(!adj.empty() && "Adjacency matrix must not be empty.");
    assert(adj.size() == adj[0].size() && "Adjacency matrix must be square.");

    queue<T> queue;
    unordered_set<T> visited;

    queue.push(start);

    while (!queue.empty()) {
        const T vtx = queue.front();
        queue.pop();

        if (visited.contains(vtx))
            continue;
        visited.insert(vtx);

        // 방문한 정점 출력
        visit(vtx);

        if (!reverse) {
            for (T u = 0; u < adj.size(); ++u) {
                if (adj[vtx][u] == true) {
                    if (!visited.contains(u)) {
                        queue.push(u);
                    }
                }
            }
        } else {
            for (T u = adj.size() - 1; u >= 0; --u) {
                if (adj[vtx][u] == true) {
                    if (!visited.contains(u)) {
                        queue.push(u);
                    }
                }
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

    vector mat(n + 1, vector(n + 1, false));

    for (int i = 0; i < e; ++i) {
        int u, v;
        cin >> u >> v;

        mat[u][v] = true;
        mat[v][u] = true;
    }

    int cnt = 1;
    vector order(n + 1, 0);
    bfs_matrix<int>(mat, s, [&](const int v) {
        order[v] = cnt++;
    }, true);

    for (int i = 1; i <= n; ++i) {
        cout << order[i] << endl;
    }

    return 0;
}