#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using edge = pair<int, int>;
const int INF = 0x3f3f3f3f;

vector<int> dijkstra(int from, int to) {
    vector<int> time(max(from, to) * 2 + 1, INF);   // 마지막 위치에서 순간이동 하는 범위까지 포함.
    time[from] = 0;

    priority_queue<edge, vector<edge>, greater<>> pq;
    pq.emplace(time[from], from);

    while (!pq.empty()) {
        auto [t, u] = pq.top();
        pq.pop();

        edge E[3] = {{1, u + 1}, {1, u - 1}, {0, 2*u}};
        for (auto [t2, u2] : E) {
            if (0 <= u2 && u2 < time.size()) {
                if (time[u2] > time[u] + t2) {
                    time[u2] = time[u] + t2;
                    pq.emplace(time[u2], u2);
                }
            }
        }
    }

    return time;
}

void $(int &n, int &k) {
    auto time = dijkstra(n, k);
    cout << time[k];
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n, k;
    cin >> n >> k;

    $(n, k);
}
