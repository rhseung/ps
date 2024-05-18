#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

vector<int> bfs(int start, vector<int> D, vector<vector<pair<int, int>>> graph) {
    queue<int> q;

    D[start] = 0;
    q.push(start);

    while (!q.empty()) {
        int v = q.front();
        q.pop();

        for (auto &[w, d] : graph[v]) {
            if (D[w] == -1) {
                D[w] = D[v] + d;
                q.push(w);
            }
        }
    }

    return D;
}

void $(int n, vector<vector<pair<int, int>>> graph) {
    vector D = bfs(1, vector<int>(n + 1, -1), graph);
    int idx = max_element(D.begin(), D.end()) - D.begin();
    D = bfs(idx, vector<int>(n + 1, -1), graph);

    cout << (*max_element(D.begin(), D.end()));
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n;
    cin >> n;

    vector<vector<pair<int, int>>> graph(n + 1, vector<pair<int, int>>());

    for (int i = 1; i < n; ++i) {
        int a, b, c;
        cin >> a >> b >> c;
        graph[a].emplace_back(b, c);
        graph[b].emplace_back(a, c);
    }

    $(n, graph);
}
