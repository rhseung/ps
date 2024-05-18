#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

void solution() {
    int n;
    cin >> n;

    int *A = new int[n];
    int *D = new int[n];

    int len = INT_MIN;

    for (int i = 0; i < n; ++i) {
        cin >> A[i];

        D[i] = 1;
        for (int j = 0; j < i; ++j) {
            if (A[i] > A[j])
                D[i] = max(D[i], D[j] + 1);
        }

        len = max(len, D[i]);
    }

    cout << len << endl;

    int now = len;
    int* S = new int[len];

    for (int i = n - 1; i >= 0; --i) {
        if (now == 0)
            break;

        if (D[i] == now) {
            S[now - 1] = A[i];
            now--;
        }
    }

    for (int i = 0; i < len; ++i)
        cout << S[i] << " ";

    delete[] A;
    delete[] D;
    delete[] S;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
