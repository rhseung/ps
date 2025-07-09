#include <bits/stdc++.h>
#define endl "\n"
#define INF 0x3f3f3f3f

using namespace std;

pair<vector<int>, bool> bellman_ford(const vector<tuple<int, int, int>> &edges, const int vtx_count, const int start) {
    vector<int> dist(vtx_count + 1, 0);
    // dist[start] = 0;

    for (int i = 0; i < vtx_count; ++i) {
        for (auto [u, v, w]: edges) {
            if (dist[u] != INF && dist[v] > dist[u] + w) {
                dist[v] = dist[u] + w;
            }
        }
    }

    bool has_cycle = false;
    for (auto [u, v, w]: edges) {
        if (dist[u] != INF && dist[v] > dist[u] + w) {
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

    int T;
    cin >> T;

    while (T--) {
        int n, road_count, wormhole_count;
        cin >> n >> road_count >> wormhole_count;

        vector<tuple<int, int, int>> edges;
        for (int i = 0; i < road_count + wormhole_count; ++i) {
            int s, e, t;
            cin >> s >> e >> t;

            if (i < road_count) {   // 도로
                edges.emplace_back(s, e, t);
                edges.emplace_back(e, s, t);
            } else {    // 웜홀
                edges.emplace_back(s, e, -t);
            }
        }

        auto [_, has_cycle] = bellman_ford(edges, n, 1);
        cout << (has_cycle ? "YES" : "NO") << endl;
    }

    return 0;
}