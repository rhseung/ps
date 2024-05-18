#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

int A[8];
int I[8];

double root = 1 / sqrt(2);
double factor[8][2] = {
    {0, 1.}, {root, root}, {1., 0}, {root, -root},
    {0, -1.}, {-root, -root}, {-1., 0}, {-root, root}
};

int ccw(int n) {
    // |a X b| = a(-b)sin45 ~= -ab
    double a_x = A[I[(n-1 + 8) % 8]] * factor[(n-1 + 8) % 8][0];
    double a_y = A[I[(n-1 + 8) % 8]] * factor[(n-1 + 8) % 8][1];
    double o_x = A[I[n]] * factor[n][0];
    double o_y = A[I[n]] * factor[n][1];
    double c_x = A[I[(n+1 + 8) % 8]] * factor[(n+1 + 8) % 8][0];
    double c_y = A[I[(n+1 + 8) % 8]] * factor[(n+1 + 8) % 8][1];

    double oa_x_ = a_x - o_x;
    double oa_y_ = a_y - o_y;
    double oc_x_ = c_x - o_x;
    double oc_y_ = c_y - o_y;

    double cross = -(oa_x_ * oc_y_ - oa_y_ * oc_x_);

    return cross == 0 ? 0 : cross > 0 ? 1 : -1;
}

int is_radial() {
    for (int i = 0; i < 8; ++i)
        if (ccw(i) != -1)  // 볼록 다각형 <=> 모든 점에서 시계 (-1)
            return 0;
    return 1;
}

void solution() {
    for (int &e : A)
        cin >> e;
    iota(I, I + 8, 0);

    int cnt = 0;
    do {
        cnt += is_radial();
    } while (next_permutation(I, I + 8));

    cout << cnt;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
