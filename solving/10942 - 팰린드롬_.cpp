// BOJ 10942 - 팰린드롬?
#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

int DP[2000][2000];

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n;
    cin >> n;

    const auto A = new int[n];
    for (int i = 0; i < n; ++i)
        cin >> A[i];

    for (int i = 0; i < n; ++i) {
        DP[i][i] = 1;
        if (i + 1 < n)
            DP[i][i + 1] = 1;

        cin >> A[i];
    }

    delete[] A;

    return 0;
}
