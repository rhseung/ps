#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n;
    cin >> n;

    deque<int> dq;
    for (int i = 0; i < n; ++i) {
        int cmd;
        cin >> cmd;

        int tmp;
        if (cmd == 1) {
            cin >> tmp;
            dq.push_front(tmp);
        }
        else if (cmd == 2) {
            cin >> tmp;
            dq.push_back(tmp);
        }
        else if (cmd == 3) {
            tmp = -1;
            if (!dq.empty()) {
                tmp = dq.front();
                dq.pop_front();
            }

            cout << tmp << endl;
        }
        else if (cmd == 4) {
            tmp = -1;
            if (!dq.empty()) {
                tmp = dq.back();
                dq.pop_back();
            }

            cout << tmp << endl;
        }
        else if (cmd == 5) {
            cout << dq.size() << endl;
        }
        else if (cmd == 6) {
            cout << (dq.empty() ? 1 : 0) << endl;
        }
        else if (cmd == 7) {
            cout << (dq.empty() ? -1 : dq.front()) << endl;
        }
        else if (cmd == 8) {
            cout << (dq.empty() ? -1 : dq.back()) << endl;
        }
    }
    
    return 0;
}
