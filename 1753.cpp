#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using edge = pair<int, int>;
const int inf = 0x3f3f3f3f;

vector<int> dijkstra(vector<vector<edge>> &graph, vector<int> &dist, int start) {
    priority_queue<edge, vector<edge>, greater<>> pq;
    pq.emplace(0, start);
    dist[start] = 0;

    while (!pq.empty()) {
        auto [w, u] = pq.top();
        pq.pop();

        for (auto &[w2, u2] : graph[u]) {
            if (dist[u2] > dist[u] + w2) {
                dist[u2] = dist[u] + w2;
                pq.emplace(dist[u2], u2);
            }
        }
    }

    return dist;
}

void $() {
    int v, e;
    cin >> v >> e;

    int start;
    cin >> start;

    vector<vector<edge>> graph(v + 1);
    vector<int> dist(v + 1, inf);

    for (int i = 0; i < e; ++i) {
        int a, b, w;
        cin >> a >> b >> w;

        graph[a].emplace_back(w, b);
    }

    dist = dijkstra(graph, dist, start);

    for (int i = 1; i <= v; ++i) {
        if (dist[i] == inf)
            cout << "INF" << endl;
        else
            cout << dist[i] << endl;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    $();
}
