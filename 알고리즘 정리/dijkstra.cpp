#include <bits/stdc++.h>
#define endl "\n"
#define INF 0x3f3f3f3f

using namespace std;

vector<int> dijkstra(const vector<vector<pair<int, int>>> &adj, const int start) {
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> priority_queue;  // 이렇게 해야 값이 작을 수록 우선 순위를 갖는 최소 힙임
    vector<int> dist(adj.size(), INF);  // visited의 역할도 동시에 할 수 있음

    priority_queue.emplace(0, start);
    dist[start] = 0;

    while (!priority_queue.empty()) {
        auto [weight, vtx] = priority_queue.top();
        priority_queue.pop();

        if (weight > dist[vtx]) continue;   // 이미 최솟값보다 커진 이상 다음 경로를 탐색할 필요가 없음

        for (auto [next_weight, next_vtx] : adj[vtx]) {
            if (dist[next_vtx] > dist[vtx] + next_weight) {
                dist[next_vtx] = dist[vtx] + next_weight;
                priority_queue.emplace(dist[next_vtx], next_vtx);
            }
        }
    }

    return dist;
}

int main() {
    // boj.kr/1916 참고, 대신 vtx는 0부터 시작하는 예제로 변형

    int vertex_count, edge_count;
    cin >> vertex_count >> edge_count;

    vector<vector<pair<int, int>>> adj(vertex_count);

    for (int i = 0; i < edge_count; ++i) {
        int u, v, weight;
        cin >> u >> v >> weight;

        adj[u].emplace_back(weight, v);
    }

    int start, end;
    cin >> start >> end;

    const vector<int> dist_from_start = dijkstra(adj, start);
    cout << dist_from_start[end] << endl;

    return 0;
}