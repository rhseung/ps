#include "../algorithms/graph.hpp"

#include <bits/stdc++.h>
#include <ranges>
#define endl "\n"
#define INF 0x3f3f3f3f

using namespace std;
typedef long long ll;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n, e, s;
    cin >> n >> e >> s;

    vector mat(n + 1, vector(n + 1, false));

    for (int i = 0; i < e; ++i) {
        int u, v;
        cin >> u >> v;

        mat[u][v] = true;
        mat[v][u] = true;
    }

    int cnt = 1;
    vector<int> order(n + 1, 0);

    graph::dfs_matrix<int>(mat, s, [&](const int u) {
        order[u] = cnt++;
    }, true);

    for (int i = 1; i <= n; ++i) {
        cout << order[i] << endl;
    }

    return 0;
}