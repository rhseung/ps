// Created by Hyunseung Ryu on 2025. 7. 21..

#include <bits/stdc++.h>
#define endl "\n"
#define INF 0x3f3f3f3f

using namespace std;
typedef long long ll;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n;
    cin >> n;

    const auto A = new int[n];
    for (int i = 0; i < n; ++i)
        cin >> A[i];

    const auto D = new int[n];
    int max_length = 1;

    for (int i = 0; i < n; ++i) {
        D[i] = 1;
        for (int j = 0; j < i; ++j) {
            if (A[j] < A[i]) {
                D[i] = max(D[i], D[j] + 1);
                max_length = max(max_length, D[i]);
            }
        }
    }

    cout << max_length;

    delete[] A;
    delete[] D;

    return 0;
}