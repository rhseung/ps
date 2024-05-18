#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

void solution() {
    int n;
    cin >> n;

    vector<vector<int>> triangle(n, vector<int>());
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j <= i; ++j) {
            int tmp;
            cin >> tmp;
            triangle[i].push_back(tmp);
        }
    }

    vector<vector<int>> sum(triangle.size(), vector<int>(triangle.size()));

    sum[0][0] = triangle[0][0];
    for (int i = 1; i < triangle.size(); ++i) {
        for (int j = 0; j <= i; ++j) {
            if (j == 0)
                sum[i][j] = sum[i - 1][j];
            else if (j == i)
                sum[i][j] = sum[i - 1][j - 1];
            else
                sum[i][j] = max(sum[i - 1][j - 1], sum[i - 1][j]);

            sum[i][j] += triangle[i][j];
        }
    }

    int max_v = INT_MIN;
    for (auto e : sum[sum.size() - 1])
        max_v = max(max_v, e);

    cout << max_v;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
