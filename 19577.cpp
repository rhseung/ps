#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

int phi(int x) {
    int ret = x;

    for (int i = 2; i * i <= x; ++i) {
        if (x % i == 0) {
            ret /= i;
            ret *= (i - 1);

            while (x % i == 0)
                x /= i;
        }
    }

    if (x != 1) {
        ret /= x;
        ret *= (x - 1);
    }

    return ret;
}

void solution() {
    int n;
    cin >> n;
    int r = INT_MAX;

    for (int x = 1; x * x <= n; ++x) {
        if (n % x == 0) {
            if (x * phi(x) == n)
                r = min(r, x);
            if (n/x * phi(n/x) == n)
                r = min(r, n/x);
        }
    }

    cout << (r == INT_MAX ? -1 : r);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
