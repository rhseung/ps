#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

void solution() {
    int n;
    cin >> n;

    int *A = new int[n];
    for (int i = 0; i < n; ++i)
        cin >> A[i];

    sort(A, A + n);

    int range = A[n - 1] - A[0];
    int median = A[n / 2];
    int sum = 0;
    unordered_map<int, int> counter;

    for (int i = 0; i < n; ++i) {
        if (counter.find(A[i]) == counter.end())
            counter[A[i]] = 0;
        counter[A[i]]++;
        sum += A[i];
    }

    int most = 0;
    for (auto p: counter) {
        most = max(most, p.second);
    }

    deque<int> mosts;
    for (auto [k, v]: counter) {
        if (v == most)
            mosts.push_back(k);
    }

    sort(mosts.begin(), mosts.end());

    cout << (int)round((double)sum / n) << endl << median << endl << (mosts.size() >= 2 ? mosts[1] : mosts[0]) << endl << range;

    delete(A);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
