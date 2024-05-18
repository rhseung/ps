#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using lnt = long long int;

#define x first
#define y second
using point = pair<int, int>;
point operator+(point& p1, point& p2) {
    return {p1.x + p2.x, p1.y + p2.y};
}
point operator-(point& p1, point& p2) {
    return {p1.x - p2.x, p1.y - p2.y};
}

template <typename T, typename U>
istream& operator>>(istream& is, pair<T, U> &p) {
    is >> p.x >> p.y;
    return is;
}

int n, k, l;
int board[100][100];

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    cin >> n >> k;
    for (int i = 0; i < k; ++i) {
        int a, b;
        cin >> a >> b;
        board[a - 1][b - 1] = 'A';
    }

    cin >> l;
    vector<pair<int, char>> L(l);
    for (auto &e : L)
        cin >> e;

    point directions[] = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};
    int direction = 0;

    deque<point> P = {{0, 0}};
    int t = 1;
    int L_cursor = 0;

    board[0][0] = 1;
    while (true) {
        point new_p = P[0] + directions[direction];
        if (!(0 <= new_p.x && new_p.x < n && 0 <= new_p.y && new_p.y < n) || find(P.begin(), P.end(), new_p) != P.end())
            break;

        P.push_front(new_p);
        if (board[P[0].x][P[0].y] == 'A') {
            board[P[0].x][P[0].y] = 0;
        }
        else {
            point b = P.back();
//            board[b.x][b.y] = 0;
            P.pop_back();
        }
        t++;

//        cout << t << "s: ";
//        for (auto &e : P)
//            cout << "(" << e.x << ", " << e.y << ") ";
//        cout << endl;
//        if (board[new_p.x][new_p.y] == 1)
//            break;

        if (L_cursor < l && L[L_cursor].first == t - 1) {
            if (L[L_cursor].second == 'D')
                direction = (direction + 1) % 4;
            else
                direction = (direction - 1 + 4) % 4;
            L_cursor++;
        }

        point new_new_p = P[0] + directions[direction];
        if (!(0 <= new_new_p.x && new_new_p.x < n && 0 <= new_new_p.y && new_new_p.y < n) || find(P.begin(), P.end(), new_new_p) != P.end())
            break;
    }

    cout << t;
}
