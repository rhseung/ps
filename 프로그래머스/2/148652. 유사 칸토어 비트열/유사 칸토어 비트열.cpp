#include <bits/stdc++.h>
#define endl "\n"
using namespace std;
using lnt = long long int;

lnt f(int n, long long k) {
    if (n == 1)
        return k <= 2 ? k : k - 1;

    /**
    n = 0: 1 (입력되지 않음)
    n = 1: 1 1 0 1 1
    n = 2: (1 1 0 1 1) (1 1 0 1 1) 00000 11011 11011
    n = 3: (11011 11011 00000 11011 11011) (11011 11011 00000 11011 11011) (00000 00000 00000 00000 00000) (11011 11011 00000 11011 11011) (11011 11011 00000 11011 11011)

    2 1 21 13

    **/

    lnt part = (lnt)pow(5, n - 1);
    lnt one = (lnt)pow(4, n - 1);

    lnt full = k / part;

    if (k % part == 0)
        full--;

    if (full < 2)
        return one * full + f(n - 1, k - full * part);
    else if (full == 2)
        return one * full;
    else
        return one * (full - 1) + f(n - 1, k - full * part);
}

lnt solution(int n, long long l, long long r) {
    lnt left = f(n, l - 1);
    lnt right = f(n, r);
//    cout << left << " " << right;

    return right - left;
}