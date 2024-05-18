#include <string>
#include <iostream>
#include <stack>

using namespace std;

bool solution(string s) {
    std::stack<char> st;
    for (auto ch : s) {
        if (ch == '(')
            st.push(ch);
        else if (ch == ')') {
            if (st.empty())
                return false;

            char v = st.top();
            st.pop();
            if (v != '(')
                return false;
        }
    }

    return st.empty();
}