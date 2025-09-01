#include <bits/stdc++.h>
#define endl "\n"
#define INF 0x3f3f3f3f

using namespace std;

void dfs(vector<vector<int>>& tree, int now, set<int>& visited, vector<int>& parents) {
    visited.insert(now);

    for (int child : tree[now]) {
        if (!visited.contains(child)) {
            dfs(tree, child, visited, parents);

            if (child >= 2) // 양방향 간선이라 1(부모)일 수도 있음
                parents[child - 2] = now;
        }
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n;
    cin >> n;

    vector<vector<int>> tree(n + 1);
    for (int i = 0; i < n - 1; ++i) {
        int u, v;
        cin >> u >> v;

        tree[u].push_back(v);
        tree[v].push_back(u);
    }

    set<int> visited;
    vector<int> parents(n - 1);
    dfs(tree, 1, visited, parents);

    for (int parent : parents) {
        cout << parent << endl;
    }

    return 0;
}