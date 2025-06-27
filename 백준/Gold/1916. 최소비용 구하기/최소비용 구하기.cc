#include <bits/stdc++.h>
#define endl "\n"
#define INF 0x3f3f3f3f

using namespace std;

vector<int> dijkstra(const vector<vector<pair<int, int>>> &adj, const int start) {
    vector<int> dist(adj.size(), INF);
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq;

    dist[start] = 0;
    pq.emplace(0, start);

    while (!pq.empty()) {
        auto [w, u] = pq.top();
        pq.pop();

        if (w > dist[u]) continue;

        for (auto [u_to_v, v] : adj[u]) {
            if (dist[v] > dist[u] + u_to_v) {
                dist[v] = dist[u] + u_to_v;
                pq.emplace(dist[v], v);
            }
        }
    }

    return dist;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n, m;
    cin >> n >> m;

    vector<vector<pair<int, int>>> adj(n + 1);

    for (int i = 0; i < m; ++i) {
        int a, b, w;
        cin >> a >> b >> w;

        adj[a].emplace_back(w, b);
    }

    int start, end;
    cin >> start >> end;

    const vector<int> dist = dijkstra(adj, start);
    cout << dist[end] << endl;

    return 0;
}