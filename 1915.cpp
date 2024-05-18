#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

int A[1000][1000];
int D[1000][1000];

void solution() {
    int n, m;
    cin >> n >> m;

    for (int i = 0; i < n; ++i) {
        string tmp;
        cin >> tmp;

        for (int j = 0; j < m; ++j) {
            A[i][j] = tmp[j] - '0';
            if (A[i][j] == 1)
                D[i][j] = 1;
        }
    }

    for (int i = 1; i < n; ++i) {
        for (int j = 1; j < m; ++j) {
            int a = D[i - 1][j], b = D[i][j - 1], c = D[i - 1][j - 1];
            if (a > 0 && b > 0 && c > 0 && D[i][j] > 0)
                D[i][j] = min(a, min(b, c)) + 1;
        }
    }

    // for (int i = 0; i < n; ++i) {
    //     for (int j = 0; j < m; ++j)
    //         cout << D[i][j] << " ";
    //     cout << endl;
    // }

    int max_val = 0;
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < m; ++j)
            max_val = max(max_val, D[i][j]);

    cout << (max_val * max_val);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
