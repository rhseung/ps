#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

void solution() {
    int n;
    cin >> n;

    int *A = new int[n];
    int *D = new int[n];

    for (int i = 0; i < n; ++i) {
        cin >> A[i];

        D[i] = 1;
        for (int j = 0; j < i; ++j) {
            if (A[i] > A[j])
                D[i] = max(D[i], D[j] + 1);
        }
    }

    int max_val = INT_MIN;
    for (int i = 0; i < n; ++i) {
        max_val = max(max_val, D[i]);
    }

    cout << max_val;

    delete(A);
    delete(D);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
