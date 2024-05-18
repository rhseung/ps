#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n;
    cin >> n;

    deque<pair<int, int>> dq;
    for (int i = 1; i <= n; ++i) {
        int tmp;
        cin >> tmp;
        dq.emplace_back(tmp, i);
    }

    int step = 0;
    while (!dq.empty()) {
        if (step == 0) {
            auto front = dq.front();
            cout << front.second << " ";
            step = front.first > 0 ? front.first - 1 : front.first;     // pop을 하면 지금 가리키던게 사라지고 자동으로 다음 걸 가리키도록 밀리기 때문에, step이 양수면 1 빼줘야 함.
            dq.pop_front();
        }
        else if (step > 0) {
            auto front = dq.front();
            dq.pop_front();
            dq.push_back(front);
            step--;
        }
        else if (step < 0) {
            auto back = dq.back();
            dq.pop_back();
            dq.push_front(back);
            step++;
        }
    }
    
    return 0;
}
