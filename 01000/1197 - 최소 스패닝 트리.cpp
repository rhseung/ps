// BOJ 1197 - 최소 스패닝 트리
#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

template <typename T> requires std::is_integral_v<T> || std::is_floating_point_v<T>
struct Edge {
    T weight;
    int from, to;

    bool operator<(const Edge& other) const {
        return weight < other.weight || (weight == other.weight && (from < other.from || (from == other.from && to < other.to)));
    }
};

// 경로 압축 최적화 적용됨
inline int find_root(std::vector<int>& parents, const int x) {
    if (x == parents[x]) return x;
    return parents[x] = find_root(parents, parents[x]);
}

// union by rank 최적화 적용됨
inline void union_root_fast(std::vector<int>& parents, std::vector<int>& ranks, int x, int y) {
    x = find_root(parents, x);
    y = find_root(parents, y);

    if (x != y) {
        if (ranks[x] < ranks[y])
            parents[x] = y;
        else if (ranks[x] > ranks[y])
            parents[y] = x;
        else {
            parents[x] = y;
            ranks[x]++;
        }
    }
}

/**
 * Kruskal 알고리즘을 사용하여 최소 스패닝 트리를 찾습니다.
 * @note <code>edges</code>는 가중치가 오름차순으로 정렬되어 있어야 합니다.
 * @tparam T
 * @param v_cnt 정점의 개수입니다. 1부터 시작하는 정점 번호를 가정합니다.
 * @param edges 가중치가 있는 간선들의 벡터입니다. 각 간선은 Edge<T> 타입입니다. 반드시 간선은 가중치가 오름차순으로 정렬되어 있어야 합니다.
 * @return 최소 스패닝 트리를 구성하는 간선들의 벡터입니다.
 */
template <typename T> requires std::is_integral_v<T> || std::is_floating_point_v<T>
std::vector<Edge<T>> kruskal(const int v_cnt, const std::vector<Edge<T>>& edges) {
    std::vector<Edge<T>> mst_edges;
    std::vector<int> parents(v_cnt + 1);
    std::vector<int> ranks(v_cnt + 1, 0);

    iota(parents.begin(), parents.end(), 0);

    for (const auto& edge : edges) {
        // If cycle detected, skip this edge
        if (find_root(parents, edge.from) == find_root(parents, edge.to)) continue;

        mst_edges.push_back(edge);
        union_root_fast(parents, ranks, edge.from, edge.to);

        // Minimum spanning tree is complete
        if (mst_edges.size() == v_cnt - 1) break;
    }

    return mst_edges;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int v_cnt, e_cnt;
    cin >> v_cnt >> e_cnt;

    vector<Edge<int>> edges(e_cnt);
    for (auto& [weight, from, to] : edges) {
        cin >> from >> to >> weight;
    }
    sort(edges.begin(), edges.end());

    vector<Edge<int>> mst_edges = kruskal(v_cnt, edges);

    cout << accumulate(mst_edges.begin(), mst_edges.end(), 0, [](const int acc, const Edge<int>& edge) {
        return acc + edge.weight;
    }) << endl;

    return 0;
}
