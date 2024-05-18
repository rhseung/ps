#include <bits/stdc++.h>
#define endl "\n"
using namespace std;

#define x first
#define y second
using point = pair<int, int>;
int dist(point p1, point p2) {
    return abs(p1.x - p2.x) + abs(p1.y - p2.y);
}

int n, m;
int city[50][50];

int min_dist(int k, vector<int> chosen, vector<point> &chickens) {
    if (k == 0) {
        int sum_dist = 0;
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                if (city[i][j] == 1) {
                    int min_of_dist = INT_MAX;
                    for (int &t : chosen)
                        min_of_dist = min(min_of_dist, dist(chickens[t], point{i, j}));

                    sum_dist += min_of_dist;
                }
            }
        }

        return sum_dist;
    }

    int min_dist_v = INT_MAX;
    for (int i = (chosen.empty() ? 0 : chosen[chosen.size() - 1] + 1); i < chickens.size(); ++i) {
        vector<int> tmp = chosen;
        tmp.push_back(i);
        min_dist_v = min(min_dist_v, min_dist(k - 1, tmp, chickens));
    }

    return min_dist_v;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n >> m;

    vector<point> chickens;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> city[i][j];
            if (city[i][j] == 2)
                chickens.emplace_back(i, j);
        }
    }

    cout << min_dist(m, vector<int>(), chickens);
}