#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using lnt = long long int;
using matrix = deque<deque<int>>;

#define MOD 1000

int n;

matrix power(matrix A, lnt p) {
    if (p == 1) return A;

    matrix half = power(A, p / 2);
    matrix half2 = half;

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            int s = 0;
            for (int k = 0; k < n; ++k)
                s = (s % MOD + (half[i][k] % MOD) * (half[k][j] % MOD) % MOD) % MOD;

            half2[i][j] = s;
        }
    }

    matrix ret = half2;
    if (p % 2 == 1) {
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                int s = 0;
                for (int k = 0; k < n; ++k)
                    s = (s % MOD + ((half2[i][k] % MOD) * (A[k][j] % MOD) % MOD)) % MOD;

                ret[i][j] = s;
            }
        }
    }

    return ret;
}

void solution() {
    lnt b;
    cin >> n >> b;

    matrix A(n, deque<int>(n));
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            cin >> A[i][j];

    matrix A_b = power(A, b);
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j)
            cout << (A_b[i][j] % MOD) << " ";
        cout << endl;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
