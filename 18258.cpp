#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n;
    cin >> n;

    queue<int> q;
    for (int i = 0; i < n; ++i) {
        string cmd;
        cin >> cmd;

        int tmp;
        if (cmd == "push") {
            cin >> tmp;
            q.push(tmp);
        }
        else if (cmd == "pop") {
            tmp = -1;
            if (!q.empty()) {
                tmp = q.front();
                q.pop();
            }

            cout << tmp << endl;
        }
        else if (cmd == "size") {
            cout << q.size() << endl;
        }
        else if (cmd == "empty") {
            cout << (q.empty() ? 1 : 0) << endl;
        }
        else if (cmd == "front") {
            tmp = q.empty() ? -1 : q.front();
            cout << tmp << endl;
        }
        else if (cmd == "back") {
            tmp = q.empty() ? -1 : q.back();
            cout << tmp << endl;
        }
    }
    
    return 0;
}
