#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

void solution() {
    int n;
    cin >> n;

    deque<int> dq;

    int* A = new int[n];
    for (int i = 0; i < n; ++i)
        cin >> A[i];

    int tmp;
    for (int i = 0; i < n; ++i) {
        cin >> tmp;

        if (A[i] == 0)
            dq.push_back(tmp);
    }

    int m;
    cin >> m;

    // for (int i = 0; i < m; ++i) {
    //     int x;
    //     cin >> x;
    //
    //     int r = x;
    //     for (int j = 0; j < n; ++j) {
    //         if (A[j] == 0) {   // queue
    //             swap(B[j], r);
    //         }
    //         // stack은 그냥 넣었다 뺐다 r = r;
    //     }
    //
    //     cout << r << " ";
    // }
    // stack은 의미가 없으므로 queue만 여러 개 있는건데, 이건 걍 긴 queue 하나와 동치임.

    for (int i = 0; i < m; ++i) {
        int x;
        cin >> x;

        // queue가 [1, 4] 로 입력된다면 나가는 건 [4, 1] 순서이니 pop_back 으로 해야됨. 스택은 아님 x가 push_front 해야됨.
        dq.push_front(x);
        cout << dq.back() << " ";
        dq.pop_back();
    }

    delete(A);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
