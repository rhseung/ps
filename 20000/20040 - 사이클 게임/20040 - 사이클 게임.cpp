// BOJ 20040 - 사이클 게임
#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

// 경로 압축 최적화 적용됨
inline int find_root(std::vector<int>& parents, const int x) {
    if (x == parents[x]) return x;
    return parents[x] = find_root(parents, parents[x]);
}

// 사이클이 발생하면 true, 아니면 false 반환
inline bool union_root(std::vector<int>& parents, int x, int y) {
    x = find_root(parents, x);
    y = find_root(parents, y);

    if (x != y) {
        parents[x] = y;
        return false;
    }
    else {
        return true;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int v_cnt, step_cnt;
    cin >> v_cnt >> step_cnt;

    vector<int> parents(v_cnt);
    iota(parents.begin(), parents.end(), 0);

    int ans = 0;
    for (int i = 0; i < step_cnt; ++i) {
        int u, v;
        cin >> u >> v;

        if (union_root(parents, u, v)) {
            ans = i + 1;
            break;
        }
    }

    cout << ans << endl;

    return 0;
}
