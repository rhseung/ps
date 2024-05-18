#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

using point = pair<int64_t, int64_t>;
using line = pair<point, point>;

int64_t ccw(point p1, point p2, point p3) {
    point v12 = {p2.first - p1.first, p2.second - p1.second};
    point v23 = {p3.first - p2.first, p3.second - p2.second};

    int64_t cross = v12.first * v23.second - v12.second * v23.first;
    return cross == 0 ? 0 : cross / abs(cross);
}

bool is_intersect(line l1, line l2) {
    point p1 = l1.first,
        p2 = l1.second,
        p3 = l2.first,
        p4 = l2.second;

    int64_t ccw_base_l1 = ccw(p1, p2, p3) * ccw(p1, p2, p4);
    int64_t ccw_base_l2 = ccw(p3, p4, p1) * ccw(p3, p4, p2);

    if (ccw_base_l1 == 0 && ccw_base_l2 == 0) {
        if (p1 > p2) swap(p1, p2);
        if (p3 > p4) swap(p3, p4);
        return p1 <= p4 && p3 <= p2;
    }

    return ccw_base_l1 <= 0 && ccw_base_l2 <= 0;
}

void solution() {
    point p1, p2, p3, p4;
    cin >> p1.first >> p1.second >> p2.first >> p2.second
        >> p3.first >> p3.second >> p4.first >> p4.second;

    line l1 = {p1, p2}, l2 = {p3, p4};
    cout << is_intersect(l1, l2);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
