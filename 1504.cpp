#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using edge = pair<int, int>;
const int inf = INT_MAX / 3;    // 경로1 + 경로2 + 경로3 가 int 범위 이려면 경로 <= int/3

vector<int> dijkstra(vector<vector<edge>> &graph, vector<int> dist, int start) {
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

    vector<vector<edge>> graph(v + 1);

    for (int i = 0; i < e; ++i) {
        int a, b, w;
        cin >> a >> b >> w;

        graph[a].emplace_back(w, b);
        graph[b].emplace_back(w, a);
    }

    int v1, v2;
    cin >> v1 >> v2;

    // 1 -> v1 -> v2 -> v 이 가까운지 1 -> v2 -> v1 -> v 인지 모름
    // 1 -> v1, 1 -> v2 ... 1에서 다익스트라
    // v1 -> v2, v1 -> v ... v1에서 다익스트라
    // v2 -> v, v2 -> v1 ... v2에서 다익스트라
    // 이렇게 구하고 더해서 경로의 최솟값을 구하기. v1 -> v2 이나, v2 -> v1이나 그래프가 양방향이라 똑같긴 함.

    auto dist_1 = dijkstra(graph, vector<int>(v + 1, inf), 1);
    int _1_to_v1 = dist_1[v1];
    int _1_to_v2 = dist_1[v2];

    auto dist_v1 = dijkstra(graph, vector<int>(v + 1, inf), v1);
    int v1_to_v2 = dist_v1[v2];
    int v1_to_v = dist_v1[v];

    auto dist_v2 = dijkstra(graph, vector<int>(v + 1, inf), v2);
    int v2_to_v1 = dist_v2[v1];
    int v2_to_v = dist_v2[v];

    int min_dist = min(_1_to_v1 + v1_to_v2 + v2_to_v, _1_to_v2 + v2_to_v1 + v1_to_v);

    cout << (min_dist >= inf ? -1 : min_dist);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    $();
}
