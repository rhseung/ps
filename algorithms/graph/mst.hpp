//
// Created by Hyunseung Ryu on 2025. 8. 14..
//

#ifndef PS_KRUSKAL_HPP
#define PS_KRUSKAL_HPP

#include "union-find.hpp"
#include "weighted_edge.hpp"

namespace graph {
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
}

#endif //PS_KRUSKAL_HPP
