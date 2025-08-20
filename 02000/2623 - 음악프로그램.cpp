// BOJ 2623 - 음악프로그램
#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

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

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n, m;
    cin >> n >> m;

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int k;
        cin >> k;

        vector<int> tmp(k);
        for (int j = 0; j < k; ++j) {
            cin >> tmp[j];
        }

        for (int j = 1; j < tmp.size(); ++j) {
            adj[tmp[j - 1]].push_back(tmp[j]);
        }
    }

    auto s = topo_kahn(n, adj);
    if (!s.has_value())
        cout << 0 << endl;
    else {
        for (const int v : s.value())
            cout << v << endl;
    }

    return 0;
}
