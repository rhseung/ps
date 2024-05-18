#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

#define SIZE 500
using uint = unsigned int;
typedef struct mat {
    int r;
    int c;
} mat;

mat M[SIZE];
uint DP[SIZE][SIZE];   // D[start][end] = start 번째 ~ end 번째 행렬 곱의 최소 연산

/**
 * A, B, C, D
 * A(BCD)
 * AB(CD)
 * ABC(D)
 */

uint topdown(int i, int j) {
    if (i == j) return 0;
    if (DP[i][j] != 0) return DP[i][j];

    uint ret = -1;
    for (int k = i; k < j; ++k)
        ret = min(ret, topdown(i, k) + topdown(k+1, j) + M[i].r * M[k+1].r * M[j].c);

    DP[i][j] = ret;
    return ret;
}

void solution() {
    int n;
    cin >> n;

    for (int i = 0; i < n; ++i)
        cin >> M[i].r >> M[i].c;

    topdown(0, n - 1);
    cout << DP[0][n - 1];
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
