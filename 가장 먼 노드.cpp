#include <bits/stdc++.h>
#define endl "\n"
using namespace std;

int max_v = INT_MIN;

vector<int> bfs(vector<vector<int>> graph, vector<int> D) {
    D[1] = 0;
    queue<int> q;
    q.push(1);

    while (!q.empty()) {
        int f = q.front();
        q.pop();

        for (auto w : graph[f]) {
            if (D[w] == -1) {
                D[w] = D[f] + 1;
                max_v = max(max_v, D[w]);
                q.push(w);
            }
        }
    }

    return D;
}

int solution(int n, vector<vector<int>> edge) {
    vector<vector<int>> graph(n + 1, vector<int>());
    vector<int> D(n + 1, -1);

    for (auto e : edge) {
        graph[e[0]].push_back(e[1]);
        graph[e[1]].push_back(e[0]);
    }

    D = bfs(graph, D);

    int cnt = 0;
    for (int i = 1; i <= n; ++i)
        if (D[i] == max_v) cnt++;

    return cnt;
}