#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using i64 = long long int;
#define MOD 1'000'000'007

i64 init(vector<i64> &T, vector<i64> &A, i64 start, i64 end, i64 root) {
    if (start == end)
        return T[root] = A[start];
    else {
        i64 mid = (start + end) / 2;
        i64 left_v = init(T, A, start, mid, 2*root);
        i64 right_v = init(T, A, mid + 1, end, 2*root + 1);
        return T[root] = (left_v * right_v) % MOD;
    }
}

i64 mul(vector<i64> &T, i64 start, i64 end, i64 root, i64 left, i64 right) {
    if (right < start || end < left)
        return 1;
    else if (left <= start && end <= right)
        return T[root];
    else {
        i64 mid = (start + end) / 2;
        i64 left_v = mul(T, start, mid, 2 * root, left, right);
        i64 right_v = mul(T, mid + 1, end, 2 * root + 1, left, right);
        return (left_v * right_v) % MOD;
    }
}

void update(vector<i64> &T, i64 start, i64 end, i64 root, i64 idx, i64 value) {
    if (!(start <= idx && idx <= end))
        return;

    if (start == end)
        T[root] = value;
    else {
        i64 mid = (start + end) / 2;
        update(T, start, mid, 2*root, idx, value);
        update(T, mid + 1, end, 2*root + 1, idx, value);
        T[root] = (T[2*root] * T[2*root + 1]) % MOD;
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

    vector<i64> T(4 * A.size());
    init(T, A, 1, n, 1);

    for (int i = 0; i < m + k; ++i) {
        i64 a, b, c;
        cin >> a >> b >> c;

        if (a == 1)
            update(T, 1, n, 1, b, c);
        else if (a == 2)
            cout << mul(T, 1, n, 1, b, c) << endl;
    }
}
