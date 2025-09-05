// BOJ 2373 - Fibonacci Game
#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

constexpr int MAX_N = 1000001;
int D[MAX_N];

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    vector<int> f;
    int f_1 = 1, f_2 = 2;
    while (true) {
        f.push_back(f_1);
        D[f_1] = f_1;
        D[f_2] = f_2;

        const int tmp = f_1 + f_2;
        f_1 = f_2;
        f_2 = tmp;

        if (f_1 >= MAX_N || f_2 >= MAX_N)
            break;
    }

    int v = 3;
    for (int i = 4; i < MAX_N; ++i) {
        if (D[i] != 0)
            v = i;
        else
            D[i] = D[i - v];
    }

    int n;
    cin >> n;

    for (int i = 0; i < f.size(); ++i) {
        if (n == f[i] || n == f[i + 1]) {
            cout << -1 << endl;
            return 0;
        }

        if (f[i] < n && n < f[i + 1]) {
            cout << D[n % f[i]] << endl;
            return 0;
        }
    }

    cout << D[n % f.back()] << endl;
    return 0;
}