#include <bits/stdc++.h>
#define endl "\n"
using namespace std;
using point = pair<int, int>;

int dist(point a, point b) {
    return abs(a.first - b.first) + abs(a.second - b.second);
}

int min_max_dist(int n, int k, vector<int> picked, vector<point> &A) {
    if (k == 0) {
        int max_distance = INT_MIN;
        for (auto p : A) {
            int distance = INT_MAX;
            for (auto i : picked)
                distance = min(distance, dist(A[i], p));

            max_distance = max(distance, max_distance);
        }

        return max_distance;
    }

    int min_distance = INT_MAX;
    for (int i = (picked.empty() ? 0 : picked[picked.size() - 1] + 1); i < n; ++i) {
        auto picked_ = picked;
        picked_.push_back(i);
        min_distance = min(min_distance, min_max_dist(n, k - 1, picked_, A));
    }

    return min_distance;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n, k;
    cin >> n >> k;

    vector<point> A(n);
    for (int i = 0; i < n; ++i)
        cin >> A[i].first >> A[i].second;

    cout << min_max_dist(n, k, vector<int>(), A);
}