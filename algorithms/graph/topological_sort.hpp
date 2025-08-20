//
// Created by Hyunseung Ryu on 2025. 8. 20..
//

#ifndef PS_TOPOLOGICAL_SORT_HPP
#define PS_TOPOLOGICAL_SORT_HPP

#include <vector>
#include <queue>
#include <optional>
#include <utility>
#include <algorithm>

namespace graph {
    // Kahn's algorithm, O(V + E).
    inline std::optional<std::vector<int>> topo_kahn(const int n, const std::vector<std::vector<int>>& adj) {
        std::vector<int> in_degree(n + 1, 0);
        for (int v = 1; v <= n; ++v) {
            for (const int u : adj[v])
                in_degree[u]++;
        }

        std::queue<int> q;
        for (int v = 1; v <= n; ++v) if (in_degree[v] == 0) q.push(v);

        std::vector<int> order;
        order.reserve(n);
        while (!q.empty()) {
            int v = q.front();
            q.pop();
            order.push_back(v);
            for (int u : adj[v]) {
                if (--in_degree[u] == 0) q.push(u);
            }
        }

        if (order.size() != n) return std::nullopt; // cycle detected
        return order;
    }

    // DFS-based topological sort with cycle detection. O(V + E).
    // Returns ordering if DAG; otherwise std::nullopt.
    inline std::optional<std::vector<int>> topo_dfs(const int n, const std::vector<std::vector<int>>& adj) {
        std::vector<int> color(n + 1, 0); // 0=unvisited, 1=visiting, 2=done
        std::vector<int> order;
        order.reserve(n);

        bool ok = true;
        auto dfs = [&](auto&& self, const int v) -> void {
            color[v] = 1;
            for (int u : adj[v]) {
                if (color[u] == 0) {
                    self(self, u);
                    if (!ok) return;
                }
                else if (color[u] == 1) {
                    ok = false; // back-edge => cycle
                    return;
                }
            }
            color[v] = 2;
            order.push_back(v);
        };

        for (int v = 1; v <= n && ok; ++v) if (color[v] == 0) dfs(dfs, v);
        if (!ok) return std::nullopt;
        std::ranges::reverse(order);
        return order;
    }
} // namespace graph

#endif //PS_TOPOLOGICAL_SORT_HPP
