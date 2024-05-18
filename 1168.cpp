#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using lnt = long long int;

int init(vector<int> &T, int start, int end, int root) {
    if (start == end)
        return T[root] = 1;
    else {
        int mid = (start + end) / 2;
        return T[root] = init(T, start, mid, 2*root) + init(T, mid + 1, end, 2*root + 1);
    }
}

int del(vector<int> &T, int start, int end, int root, int k) {
    int mid = (start + end) / 2;
    T[root] -= 1;

    if (start == end)
        return start;

    if (T[2*root] < k)
        return del(T, mid + 1, end, 2*root + 1, k - T[2*root]);
    else
        return del(T, start, mid, 2*root, k);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n, k;
    cin >> n >> k;

    vector<int> T(4*(n + 1));
    init(T, 1, n, 1);

    int idx = k - 1;
    cout << "<";
    for (int i = 1; i <= n; ++i) {
        cout << del(T, 1, n, 1, idx + 1);
        if (i != n) {
            cout << ", ";
            idx = (idx + k - 1) % (T[1]);
        }
    }
    cout << ">";

    return 0;
}
