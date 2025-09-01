// BOJ 11920 - 버블 정렬
#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

int arr[500000];

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n, k;
    priority_queue<int, vector<int>, greater<>> pq;

    cin >> n >> k;
    for (int i = 0; i < n; ++i) {
        cin >> arr[i];
    }

    for (int i = 0; i < k; ++i) {
        pq.push(arr[i]);
    }

    for (int i = k; i < n; ++i) {
        pq.push(arr[i]);
        arr[i - k] = pq.top();
        pq.pop();
    }

    for (int i = 0; i < n - k; ++i) {
        cout << arr[i] << " ";
    }

    while (!pq.empty()) {
        cout << pq.top() << " ";
        pq.pop();
    }

    return 0;
}
