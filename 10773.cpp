#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    
    int N;
    cin >> N;

    int sum = 0;
    stack<int> st;

    for (int i = 0; i < N; ++i) {
        int Z;
        cin >> Z;

        if (Z == 0) {
            sum -= st.top();
            st.pop();
        }
        else {
            sum += Z;
            st.push(Z);
        }
    }

    cout << sum << endl;
    
    return 0;
}
