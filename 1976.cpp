#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

int find_(int *S, int x) {
    if (x == S[x]) return x;
    else return S[x] = find_(S, S[x]);
}

void union_(int *S, int a, int b) {
    a = find_(S, a);
    b = find_(S, b);

    if (a == b)
        return;
    else if (a < b)
        S[b] = a;
    else
        S[a] = b;
}

void $(int n, int m, const int *S, const int *M) {
    int root = S[M[0]];
    for (int i = 1; i < m; ++i) {
        if (root != S[M[i]]) {
            cout << "NO";
            return;
        }
    }

    cout << "YES";
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n, m;
    cin >> n >> m;

    int *S = new int[n + 1];
    iota(S, S + n + 1, 0);

    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= n; ++j) {
            int is;
            cin >> is;

            if (is)
                union_(S, i, j);
        }
    }

    int *M = new int[m];
    for (int i = 0; i < m; ++i)
        cin >> M[i];

    $(n, m, S, M);

    delete[] S;
    delete[] M;
}
