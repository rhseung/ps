#include <bits/stdc++.h>
#define endl "\n"
using namespace std;

int solution(vector<vector<int>> triangle) {
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

    return max_v;
}