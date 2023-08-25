#include <bits/stdc++.h>
#include <ranges>

#define endl '\n'
#define setup ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr); cout << fixed; cout.precision(6);
using namespace std;
using lnt = long long int;
using uint = unsigned int;

int main() { setup;
    string str, explosive, tmp = "";
    cin >> str >> explosive;

    bool check = false;
    for (int i = 0; i < str.length(); ++i) {
        tmp += str[i];

        if (tmp.size() < explosive.size()) continue;

        check = true;
        if (tmp.back() == explosive.back()) {
            for (int j = tmp.size() - explosive.size(); j < tmp.size(); ++j) {
                if (tmp[j] != explosive[j - (tmp.size() - explosive.size())]) {
                    check = false;
                    break;
                }
            }

            if (check) {
                tmp.erase(tmp.size() - explosive.size(), explosive.size());
            }
        }
    }

    if (tmp.empty()) cout << "FRULA";
    else cout << tmp;

    return 0;
}