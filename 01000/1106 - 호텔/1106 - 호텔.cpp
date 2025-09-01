// BOJ 1106 - 호텔
#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int min_plus_customer, city_count;
    cin >> min_plus_customer >> city_count;

    vector<int> dp(min_plus_customer + 100, INT_MAX);
    dp[0] = 0;

    for (int i = 0; i < city_count; i++) {
        int cost, plus_customer;
        cin >> cost >> plus_customer;

        // dp에 계속 각 도시들의 값들을 누적하면서 모든 dp[customer]을 최소화함
        for (int customer = plus_customer; customer < dp.size(); ++customer) {
            if (dp[customer - plus_customer] != INT_MAX) {
                dp[customer] = min(dp[customer], dp[customer - plus_customer] + cost);
            }
        }
    }

    int min_cost = INT_MAX;
    for (int i = min_plus_customer; i < dp.size(); ++i) {
        min_cost = min(min_cost, dp[i]);
    }

    cout << min_cost;

    return 0;
}
