#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

int find_(int* S, int x) {
    if (x == S[x]) return x;
    else return S[x] = find_(S, S[x]);
}

void union_(int* S, int x, int y) {
    x = find_(S, x);
    y = find_(S, y);

    if (x == y)
        return;
    else if (x < y)     // 루트를 작은 것으로 합치기로 하자
        S[y] = x;
    else
        S[x] = y;
}

void $(int n, int m, int *S) {
    for (int i = 0; i < m; ++i) {
        int c, a, b;
        cin >> c >> a >> b;

        if (c == 0)
            union_(S, a, b);
        else
            cout << (find_(S, a) == find_(S, b) ? "YES" : "NO") << endl;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n, m;
    cin >> n >> m;

    int* S = new int[n + 1];
    iota(S, S + n + 1, 0);

    $(n, m, S);

    delete[] S;
}
