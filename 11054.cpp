#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

void solution() {
    int n;
    cin >> n;

    int *A = new int[n];
    int *D1 = new int[n];
    int *D2 = new int[n];

    for (int i = 0; i < n; ++i) {
        cin >> A[i];
        D1[i] = 1;
        D2[i] = 1;
    }

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < i; ++j) {
            if (A[i] > A[j])
                D1[i] = max(D1[i], D1[j] + 1);
        }
    }

    for (int i = n - 1; i >= 0; --i) {
        for (int j = n - 1; j > i; --j) {
            if (A[i] > A[j])
                D2[i] = max(D2[i], D2[j] + 1);
        }
    }

    // for (int i = 0; i < n; ++i)
    //     cout << D1[i] << " ";
    // cout << endl;
    // for (int i = 0; i < n; ++i)
    //     cout << D2[i] << " ";

    int max_val = INT_MIN;
    for (int i = 0; i < n; ++i) {
        max_val = max(max_val, D1[i] + D2[i] - 1);
    }

    cout << max_val;

    delete A;
    delete D1;
    delete D2;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
