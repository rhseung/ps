#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

int n, m;
deque<int> buf(m + 1, 0);

void dfs(int before, int depth) {
    if (depth == m) {
        for (int i = 1; i <= m; ++i)
            cout << buf[i] << " ";
        cout << endl;
    }
    else {
        for (int a = before; a <= n; ++a) {
            buf[depth + 1] = a;
            dfs(a, depth + 1);
        }
    }
}

void solution() {
    cin >> n >> m;

    dfs(1, 0);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
