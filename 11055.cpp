#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

void solution() {
    int n;
    cin >> n;

    int* A = new int[n];
    int* D = new int[n];

    int max_v = INT_MIN;

    for (int i = 0; i < n; ++i) {
        cin >> A[i];

        D[i] = A[i];
        for (int j = 0; j < i; ++j) {
            if (A[i] > A[j]) {
                D[i] = max(D[i], D[j] + A[i]);
            }
        }

        max_v = max(max_v, D[i]);
    }

    cout << max_v;

    delete[] A;
    delete[] D;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
