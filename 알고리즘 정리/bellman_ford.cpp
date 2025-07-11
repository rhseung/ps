#include <bits/stdc++.h>
#define endl "\n"
#define INF 0x3f3f3f3f

using namespace std;

pair<vector<int>, bool> bellman_ford(const vector<tuple<int, int, int>> &edges, const int vtx_count, const int start) {
    vector<int> dist(vtx_count + 1, INF);
    dist[start] = 0;

    for (int i = 0; i < vtx_count; ++i) {   // 정점 개수만큼 루프 O(VE)
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

    return 0;
}