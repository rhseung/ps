// BOJ 1922 - 네트워크 연결
#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

/**
 * Prim 알고리즘을 사용하여 최소 스패닝 트리를 찾습니다. Prim 알고리즘은 그래프 내에 많은 숫자의 간선을 가지는 ‘밀집 그래프(Dense Graph)’의 경우 적합합니다. 시간 복잡도 O(E log V)입니다.
 * @tparam T
 * @param v_cnt 정점의 개수입니다. 1부터 시작하는 정점 번호를 가정합니다.
 * @param graph 인접 리스트 형태로 표현된 그래프입니다. 각 요소는 가중치가 있는 간선의 벡터입니다. 각 간선은 pair<T, int> 형태로, T는 가중치, int는 연결된 정점의 번호입니다.
 * @param start 시작 정점의 번호입니다. 기본값은 1입니다. Prim 알고리즘은 시작 정점에서부터 최소 스패닝 트리를 확장합니다.
 * @return 최소 스패닝 트리를 구성하는 간선들의 벡터입니다. 각 요소는 pair<T, int> 형태로, T는 가중치, int는 연결된 정점의 번호입니다.
 */
template <typename T> requires std::integral<T> || std::floating_point<T>
std::vector<pair<T, int>> prim(const int v_cnt, const std::vector<std::vector<pair<T, int>>>& graph, const int start = 1) {
    std::priority_queue<pair<T, int>, std::vector<pair<T, int>>, std::greater<>> pq;
    std::vector<bool> visited(v_cnt + 1, false);
    std::vector<pair<T, int>> mst_vertices;

    visited[start] = true;
    for (const auto& neighbor : graph[start])
        pq.push(neighbor);

    int cnt = 0;
    while (cnt < v_cnt - 1 && !pq.empty()) {
        auto [current_weight, current_vertex] = pq.top();
        pq.pop();

        if (visited[current_vertex]) continue;
        visited[current_vertex] = true;
        cnt++;

        mst_vertices.emplace_back(current_weight, current_vertex);

        for (const auto& neighbor : graph[current_vertex]) {
            if (!visited[neighbor.second]) {
                pq.push(neighbor);
            }
        }
    }

    return mst_vertices;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int v_cnt, e_cnt;
    cin >> v_cnt >> e_cnt;

    vector<vector<pair<int, int>>> graph(v_cnt + 1);
    for (int i = 0; i < e_cnt; ++i) {
        int u, v, w;
        cin >> u >> v >> w;

        graph[u].emplace_back(w, v);
        graph[v].emplace_back(w, u);
    }

    auto mst = prim(v_cnt, graph);

    cout << accumulate(mst.begin(), mst.end(), 0, [](const int acc, const pair<int, int>& edge) {
        return acc + edge.first;
    }) << endl;

    return 0;
}
