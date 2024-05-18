#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

#define INF 0x3f3f3f3f
using i64 = long long int;

pair<vector<i64>, bool> bellman_ford(vector<tuple<int, int, int>> &edges, int n, int start) {
    vector<i64> dist(n + 1, INF);
    dist[start] = 0;

    for (int i = 0; i < n; ++i) {   // 정점 개수만큼 루프 O(VE)
        for (auto [u, v, w] : edges) {
            if (dist[u] != INF && dist[v] > dist[u] + w)    // 검색된 적 없는 INF 노드로부터의 거리 계산은 제외
                dist[v] = dist[u] + w;
        }
    }

    bool has_cycle = false;
    for (auto [u, v, w] : edges) {
        if (dist[u] != INF && dist[v] > dist[u] + w) {    // 계속 dist가 감소 -> 음의 사이클
            has_cycle = true;
            break;
        }
    }

    return {dist, has_cycle};
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n, m;
    cin >> n >> m;

    vector<tuple<int, int, int>> edges(m);
    for (int i = 0; i < m; ++i) {
        cin >> get<0>(edges[i]) >> get<1>(edges[i]) >> get<2>(edges[i]);
    }

    auto [dist, has_cycle] = bellman_ford(edges, n, 1);

    if (has_cycle)
        cout << -1;
    else {
        for (int i = 2; i <= n; ++i) {
            if (dist[i] == INF)
                cout << -1 << endl;
            else
                cout << dist[i] << endl;
        }
    }
}
