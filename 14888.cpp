#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

int n;
int A[11];
int O[10];

int max_val = -1'000'000'000;
int min_val = 1'000'000'000;

void dfs(int op[], int depth) {
    if (depth == n - 1) {
        int val = A[0];
        for (int i = 0; i < n - 1; ++i) {
            if (O[i] == 0)
                val += A[i + 1];
            else if (O[i] == 1)
                val -= A[i + 1];
            else if (O[i] == 2)
                val *= A[i + 1];
            else if (O[i] == 3)
                val /= A[i + 1];
        }

        max_val = max(max_val, val);
        min_val = min(min_val, val);

        return;
    }

    for (int i = 0; i < 4; ++i) {
        if (op[i] > 0) {
            O[depth] = i;
            op[i] -= 1;
            dfs(op, depth + 1);
            op[i] += 1;
            O[depth] = -1;
        }
    }
}

void solution() {
    memset(O, -1, sizeof(O));

    cin >> n;
    for (int i = 0; i < n; ++i) cin >> A[i];

    int op[4];
    cin >> op[0] >> op[1] >> op[2] >> op[3];
    dfs(op, 0);

    cout << max_val << endl << min_val;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
