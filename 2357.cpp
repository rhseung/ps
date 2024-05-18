#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using lnt = long long int;

#define INF LONG_LONG_MAX

pair<lnt, lnt> init(vector<pair<lnt, lnt>> &T, vector<lnt> &A, lnt start, lnt end, lnt root) {
    if (start == end)
        return T[root] = {A[start], A[start]};
    else {
        lnt mid = (start + end) / 2;
        auto left = init(T, A, start, mid, 2*root);
        auto right = init(T, A, mid + 1, end, 2*root + 1);
        return T[root] = {min(left.first, right.first), max(left.second, right.second)};
    }
}

pair<lnt, lnt> interval(vector<pair<lnt, lnt>> &T, lnt start, lnt end, lnt root, lnt left, lnt right) {
    if (end < left || right < start)
        return {INF, 0};
    else if (left <= start && end <= right)
        return T[root];
    else {
        lnt mid = (start + end) / 2;
        auto left_v = interval(T, start, mid, 2*root, left, right);
        auto right_v = interval(T, mid + 1, end, 2*root + 1, left, right);
        return {min(left_v.first, right_v.first), max(left_v.second, right_v.second)};
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n, m;
    cin >> n >> m;

    vector<lnt> A(n + 1);
    for (int i = 1; i <= n; ++i)
        cin >> A[i];

    vector<pair<lnt, lnt>> T(4 * A.size());
    init(T, A, 1, n, 1);

    for (int i = 0; i < m; ++i) {
        lnt a, b;
        cin >> a >> b;

        auto v = interval(T, 1, n, 1, a, b);
        cout << v.first << " " << v.second << endl;
    }
}
