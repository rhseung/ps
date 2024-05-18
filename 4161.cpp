#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

typedef struct pos {
    int x, y;
} pos;

struct pos_hash {
    size_t operator() (const pos &p) const {
        auto hash1 = hash<int>{}(p.x);
        auto hash2 = hash<int>{}(p.y);
        return hash1 ^ hash2;
    }
};

int pre[4][4] = {
    {0, 3, 2, 5},
    {3, 4, 1, 2},
    {2, 1, 4, 3},
    {5, 2, 3, 2}
};

int tour(int x, int y, int end_x, int end_y) {
    if (abs(end_x - x) <= 3 && abs(end_y - y) <= 3) {
        return pre[abs(end_x - x)][abs(end_y - y)];
    }

    if (y > end_y)
        return min(tour(x + 1, y - 2, end_x, end_y), tour(x + 2, y - 1, end_x, end_y)) + 1;
    else
        return min(tour(x + 1, y + 2, end_x, end_y), tour(x + 2, y + 1, end_x, end_y)) + 1;
}

int gcd(int a, int b) {
    if (!b) return a;
    return gcd(b, a % b);
}

void solution() {
    int end_x, end_y;

    while (cin >> end_x >> end_y) {
        end_x = abs(end_x);
        end_y = abs(end_y);
        int g = end_x != 0 && end_y != 0 ? gcd(end_x, end_y) : 1;
        cout << (g * tour(0, 0, end_x / g, end_y / g)) << endl;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
