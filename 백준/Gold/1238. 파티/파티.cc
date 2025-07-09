#include <bits/stdc++.h>
#define endl "\n"
#define INF 0x3f3f3f3f

using namespace std;

vector<int> dijkstra(const vector<vector<pair<int, int>>> &adj, const int start) {
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq;
    vector<int> dist(adj.size(), INF);

    pq.emplace(0, start);
    dist[start] = 0;

    while (!pq.empty()) {
        auto [w, vtx] = pq.top();
        pq.pop();

        if (w > dist[vtx]) continue;

        for (auto [next_w, next_vtx] : adj[vtx]) {
            if (dist[next_vtx] > dist[vtx] + next_w) {
                dist[next_vtx] = dist[vtx] + next_w;
                pq.emplace(dist[next_vtx], next_vtx);
            }
        }
    }

    return dist;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n, m, x;
    cin >> n >> m >> x;

    vector<vector<pair<int, int>>> G(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v, w;
        cin >> u >> v >> w;

        G[u].emplace_back(w, v);
    }

    int max_weight = INT_MIN;
    const vector<int> x_to_home = dijkstra(G, x);

    for (int i = 1; i <= n; ++i) {
        int i_to_x = dijkstra(G, i)[x];
        int weight = i_to_x + x_to_home[i];

        if (weight > max_weight)
            max_weight = weight;
    }

    cout << max_weight << endl;

    return 0;
}