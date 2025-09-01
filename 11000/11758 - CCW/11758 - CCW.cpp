//
// Created by Hyunseung Ryu on 2025. 7. 21..
//

#include <bits/stdc++.h>
#define endl "\n"
#define INF 0x3f3f3f3f
#define x first
#define y second

using namespace std;
typedef long long ll;
typedef pair<ll, ll> point;

/**
 * CCW (Counter Clock Wise) - 세 점의 방향을 구합니다.
 * @param p1 첫 번째 점
 * @param p2 두 번째 점
 * @param p3 세 번째 점
 * @return <b>0</b>: 세 점이 일직선상에 있을 때, <b>1</b>: p1 -> p2 -> p3가 반시계 방향일 때, <b>-1</b>: 시계 방향일 때
 */
inline ll ccw(const point &p1, const point &p2, const point &p3) {
    const point vector_12 = {p2.x - p1.x, p2.y - p1.y};
    const point vector_23 = {p3.x - p2.x, p3.y - p2.y};
    const ll cross_product = vector_12.x * vector_23.y - vector_12.y * vector_23.x;

    return cross_product == 0 ? 0 : (cross_product > 0 ? 1 : -1);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    point p1, p2, p3;
    cin >> p1.x >> p1.y >> p2.x >> p2.y >> p3.x >> p3.y;
    cout << ccw(p1, p2, p3) << endl;

    return 0;
}