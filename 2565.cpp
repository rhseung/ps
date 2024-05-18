#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using i32 = int32_t;
using i64 = int64_t;

void solution() {
    int n;
    cin >> n;

    auto* W = new pair<int, int>[n];
    for (int i = 0; i < n; ++i)
        cin >> W[i].first >> W[i].second;

    sort(W, W + n);

    // 왼쪽에 대해 정렬한 상태로 오른쪽을 보면:
    // 교차되지 않는 상황이라면 특정 전깃줄 위의 전깃줄 개수를 세면 증가 수열이여야함.
    // LIS

    // 교차한다 <=> w1.first < w2.first && w1.second > w2.second

    int* D = new int[n]{};
    int len = INT_MIN;

    for (int i = 0; i < n; ++i) {
        D[i] = 1;
        for (int j = 0; j < i; ++j) {
            if (W[i].second > W[j].second)
                D[i] = max(D[i], D[j] + 1);
        }

        len = max(len, D[i]);
    }

    cout << (n - len);

    delete[] W;
    delete[] D;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
