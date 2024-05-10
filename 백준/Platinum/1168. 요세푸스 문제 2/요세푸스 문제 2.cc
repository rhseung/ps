#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using lnt = long long int;

int T[400001];

int init(int start, int end, int root) {
    if (start == end)
        return T[root] = 1;
    else {
        int mid = (start + end) / 2;
        return T[root] = init(start, mid, 2*root) + init(mid + 1, end, 2*root + 1);
    }
}

int del(int start, int end, int root, int k) {
    int mid = (start + end) / 2;
    T[root] -= 1;

    if (start == end)
        return start;

    if (T[2*root] < k)
        return del(mid + 1, end, 2*root + 1, k - T[2*root]);
    else
        return del(start, mid, 2*root, k);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n, k;
    cin >> n >> k;

    init(1, n, 1);

    int idx = k - 1;
    cout << "<";
    for (int i = 1; i <= n; ++i) {
        int t = del(1, n, 1, idx + 1);
        cout << t;
        if (i != n)
            cout << ", ";
//
        if (i == n)
            break;
        idx = (idx + k - 1) % (T[1]);
    }
    cout << ">";

    return 0;
}
