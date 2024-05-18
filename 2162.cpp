#include <bits/stdc++.h>
#define endl "\n"
using namespace std;

using point = pair<int, int>;
using line = pair<point, point>;
#define x first
#define y second
istream& operator>>(istream &is, point &p) {
    is >> p.x >> p.y;
    return is;
}
#define SIZE 3000

int n;
line lines[SIZE + 1];

int ccw(point p1, point p2, point p3) {
    point v12 = {p2.first - p1.first, p2.second - p1.second};
    point v23 = {p3.first - p2.first, p3.second - p2.second};

    int cross = v12.first * v23.second - v12.second * v23.first;
    return cross == 0 ? 0 : cross / abs(cross);
}

bool is_intersect(line l1, line l2) {
    point p1 = l1.first,
        p2 = l1.second,
        p3 = l2.first,
        p4 = l2.second;

    int ccw_base_l1 = ccw(p1, p2, p3) * ccw(p1, p2, p4);
    int ccw_base_l2 = ccw(p3, p4, p1) * ccw(p3, p4, p2);

    if (ccw_base_l1 == 0 && ccw_base_l2 == 0) {
        if (p1 > p2) swap(p1, p2);
        if (p3 > p4) swap(p3, p4);
        return p1 <= p4 && p3 <= p2;
    }

    return ccw_base_l1 <= 0 && ccw_base_l2 <= 0;
}

int parent[SIZE + 1];
int N[SIZE + 1];

int find_(int u) {
    if (u == parent[u]) return u;
    else return parent[u] = find_(parent[u]);
}

void union_(int a, int b) {
    a = find_(a);
    b = find_(b);

    if (a == b)
        return;
    else if (a < b) {
        parent[b] = a;
        N[a] += N[b];
    }
    else {
        parent[a] = b;
        N[b] += N[a];
    }
}

bool visited[SIZE + 1];

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    fill(N + 1, N + SIZE + 1, 1);
    iota(parent + 1, parent + SIZE + 1, 1);

    cin >> n;
    for (int i = 1; i <= n; ++i)
        cin >> lines[i].first >> lines[i].second;

    for (int i = 1; i <= n; ++i)
        for (int j = i + 1; j <= n; ++j)
            if (is_intersect(lines[i], lines[j]))
                union_(i, j);

    for (int i = 1; i <= n; ++i)
        parent[i] = find_(parent[i]);

    int cnt = 0, max_len = 0;
    for (int i = 1; i <= n; ++i) {
        max_len = max(max_len, N[parent[i]]);
        if (!visited[parent[i]]) {
            visited[parent[i]] = true;
            cnt++;
        }
    }

    cout << cnt << endl << max_len;
}