#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using lnt = long long int;

// leaf: n <= 2'000'000 < 2^21
// all: 2^0 + 2^1 + 2^2 + ... + 2^21 = 2^22 - 1
int C[2'000'000 + 1];
int T[1 << 22];

void update(int start, int end, int root, int idx, int diff) {
    if (!(start <= idx && idx <= end))
        return;

    T[root] += diff;
    if (start != end) {
        int mid = (start + end) / 2;
        update(start, mid, 2*root, idx, diff);
        update(mid + 1, end, 2*root + 1, idx, diff);
    }
}

int del(int start, int end, int root, int x) {
    int mid = (start + end) / 2;
    T[root] -= 1;

    if (start == end)
        return start;

    if (T[2*root] < x)
        return del(mid + 1, end, 2*root + 1, x - T[2 * root]);
    else {
        return del(start, mid, 2*root, x);
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n;
    cin >> n;

    while (n--) {
        int t, x;
        cin >> t >> x;

        if (t == 1) {
            C[x] += 1;
            update(1, 2'000'000, 1, x, 1);
        }
        else if (t == 2) {
            cout << del(1, 2000000, 1, x) << endl;
        }
    }
}
