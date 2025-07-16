#include <bits/stdc++.h>
#define endl "\n"
#define INF 0x3f3f3f3f

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n;
    cin >> n;

    vector<pair<int, int>> intervals(n);
    for (int i = 0; i < n; i++) {
        cin >> intervals[i].first >> intervals[i].second;
    }

    // 정렬된다는 조건이 없음
    ranges::sort(intervals);

    priority_queue<int, vector<int>, greater<>> pq;
    for (auto &[s, t] : intervals) {
        pq.push(t);
        if (pq.top() <= s) pq.pop();
    }

    cout << pq.size() << endl;

    return 0;
}