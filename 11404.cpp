#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using i64 = long long int;
#define INF 0x3f3f3f3f

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n, m;
    cin >> n >> m;

    vector<vector<int>> D(n + 1, vector<int>(n + 1, INF));

    for (int i = 1; i <= n; ++i)
        D[i][i] = 0;

    for (int i = 0; i < m; ++i) {
        int a, b, c;
        cin >> a >> b >> c;
        D[a][b] = min(D[a][b], c);  // 시작 도시와 도착 도시를 연결하는 노선은 하나가 아닐 수 있다.
    }

    // Floyd-Warshall
    for (int k = 1; k <= n; ++k) {
        for (int i = 1; i <= n; ++i)
            for (int j = 1; j <= n; ++j)
                D[i][j] = min(D[i][j], D[i][k] + D[k][j]);
    }

    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= n; ++j) {
            if (D[i][j] == INF)
                cout << 0 << " ";
            else
                cout << D[i][j] << " ";
        }
        cout << endl;
    }
}
