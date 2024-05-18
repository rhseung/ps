#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int N;
    cin >> N;

    stack<int> st;

    for (int i = 0; i < N; ++i) {
        int cmd;
        cin >> cmd;

        int tmp;
        switch (cmd) {
            case 1:
                cin >> tmp;
                st.push(tmp);
                break;
            case 2:
                tmp = -1;
                if (!st.empty()) {
                    tmp = st.top();
                    st.pop();
                }

                cout << tmp << endl;
                break;
            case 3:
                cout << st.size() << endl;
                break;
            case 4:
                cout << (st.empty() ? 1 : 0) << endl;
                break;
            case 5:
                tmp = st.empty() ? -1 : st.top();
                cout << tmp << endl;
                break;
            default: ;
        }
    }

    return 0;
}
