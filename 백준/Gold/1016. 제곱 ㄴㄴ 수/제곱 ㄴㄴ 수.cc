#include <bits/stdc++.h>
#define endl "\n"
using namespace std;

void solve() {
    long long int min, max;
    cin >> min >> max;

    vector<bool> v(max - min + 1, true);
    long long int count = max - min + 1;
    
    for (long long int x = 2; x * x <= max; x++) {
        long long int temp = (min / (x * x) + (min % (x * x) != 0)) * x * x;

        if (temp <= max) {
            for (long long int y = 0; temp + y * (x * x) <= max; y++) {
                if (v[temp + y * (x * x) - min] == true) {
                    v[temp + y * (x * x) - min] = false;
                    count--;
                }
            }
        }
    }
    
    cout << count;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    // cout << fixed;
    // cout.precision(6);

    //int T; cin >> T; while (T--) 
    {
        solve();
    }

    return 0;
}