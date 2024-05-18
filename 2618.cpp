#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using lnt = long long int;

using point = pair<int, int>;
#define x first
#define y second

int n, w;
int DP[1001][1001];
int DP_trace[1001][1001];
point tasks[1001];

int dist(point p1, point p2) {
    return abs(p1.x - p2.x) + abs(p1.y - p2.y);
}

int top_down(int i, int j) {
    int k = max(i, j) + 1;

    if (k == w + 1)
        return 0;
    if (DP[i][j] != -1)
        return DP[i][j];

    int police1 = top_down(k, j) + dist(tasks[k], i == 0 ? point{1, 1} : tasks[i]);
    int police2 = top_down(i, k) + dist(tasks[k], j == 0 ? point{n, n} : tasks[j]);

    DP[i][j] = min(police1, police2);
    DP_trace[i][j] = police1 < police2 ? 1 : 2;

    return DP[i][j];
}

/**
 * DP[i][j] = 경찰차1이 i번째 사건을, 경찰차2가 j번째 사건을 해결했을 때 경로의 합.
 *
 * 경찰차1이 다음 사건을 해결하는 경우: 새 사건 번호 k = max(i, j) + 1
 * DP[i][j] + distance(tasks[k], tasks[i]) = DP[k][j]
 *
 * 경찰차2가 다음 사건을 해결하는 경우: 새 사건 번호 k = max(i, j) + 1
 * DP[i][j] + distance(tasks[k], tasks[j]) = DP[i][k]
 */

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> w;
    for (int i = 1; i <= w; ++i)
        cin >> tasks[i].x >> tasks[i].y;

    memset(DP, -1, sizeof(DP));
    cout << top_down(0, 0) << endl;

    int i = 0, j = 0;
    for (int t = 0; t < w; ++t) {
        int trace = DP_trace[i][j];
        cout << trace << endl;

        if (trace == 1)
            i = max(i, j) + 1;
        else if (trace == 2)
            j = max(i, j) + 1;
    }
}
