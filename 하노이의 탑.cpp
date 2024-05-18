#include <string>
#include <vector>
#include <algorithm>

using namespace std;
vector<vector<int>> ret;

void hanoi(int n, int from, int to, int tmp) {
    if (n == 1)
        ret.push_back({from, to});
    else {
        hanoi(n - 1, from, tmp, to);
        ret.push_back({from, to});
        hanoi(n - 1, tmp, to, from);
    }
}

vector<vector<int>> solution(int n) {
    hanoi(n, 1, 3, 2);
    // reverse(ret.begin(), ret.end());
    return ret;
}