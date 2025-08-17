//
// Created by Hyunseung Ryu on 2025. 8. 14..
//

#ifndef PS_KRUSKAL_HPP
#define PS_KRUSKAL_HPP

#include <numeric>

#include "union-find.hpp"
#include "unit.hpp"

namespace graph {
    /**
     * Kruskal 알고리즘을 사용하여 최소 스패닝 트리를 찾습니다. 그래프 내에 적은 숫자의 간선만을 가지는 ‘희소 그래프(Sparse Graph)’의 경우 Kruskal 알고리즘이 적합합니다. 시간 복잡도 O(E log E)입니다.
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

        std::iota(parents.begin(), parents.end(), 0);

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
}

#endif //PS_KRUSKAL_HPP
