#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using i64 = long long int;

i64 init(vector<i64> &T, vector<i64> &A, i64 start, i64 end, i64 root) {
    if (start == end)
        return T[root] = A[start];
    else {
        i64 mid = (start + end) / 2;
        return T[root] = init(T, A, start, mid, 2 * root) + init(T, A, mid + 1, end, 2 * root + 1);
    }
}

i64 sum(vector<i64> &T, i64 start, i64 end, i64 root, i64 left, i64 right) {
    if (end < left || right < start)    // (start < end < left < right) or (left < right < start < end)
        return 0;
    else if (left <= start && end <= right)
        return T[root];
    else {
        i64 mid = (start + end) / 2;
        return sum(T, start, mid, 2 * root, left, right) + sum(T, mid + 1, end, 2 * root + 1, left, right);
    }
}

void update(vector<i64> &T, i64 start, i64 end, i64 root, i64 idx, i64 value) {
    if (!(start <= idx && idx <= end))
        return;

    if (start == end)
        T[root] = value;
    else {
        i64 mid = (start + end) / 2;
        update(T, start, mid, 2 * root, idx, value);
        update(T, mid + 1, end, 2 * root + 1, idx, value);
        T[root] = T[2*root] + T[2*root + 1];
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n, m, k;
    cin >> n >> m >> k;

    vector<i64> A(n + 1);
    for (int i = 1; i <= n; ++i)
        cin >> A[i];

    vector<i64> T(4 * (n + 1));
    init(T, A, 1, n, 1);

    for (int i = 0; i < m + k; ++i) {
        i64 a, b, c;
        cin >> a >> b >> c;

        if (a == 1) {
//            i64 diff = c - A[b];
//            A[b] = c;
            update(T, 1, n, 1, b, c);
        }
        else if (a == 2)
            cout << sum(T, 1, n, 1, b, c) << endl;
    }
}
