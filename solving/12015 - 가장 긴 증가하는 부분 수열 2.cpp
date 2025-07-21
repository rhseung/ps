#include <bits/stdc++.h>
#define endl "\n"
#define INF 0x3f3f3f3f

using namespace std;
typedef long long ll;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    
    int n;
    cin >> n;
    
    auto A = new int[n];
    for (int i = 0; i < n; ++i)
        cin >> A[i];
    
    delete A;

    return 0;
}
