#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using lnt = long long int;

lnt surface(vector<lnt> &A, int left, int right) {
    if (left == right)
        return A[left];

    int mid = (left + right) / 2;
    lnt left_surface = surface(A, left, mid);
    lnt right_surface = surface(A, mid + 1, right);
    lnt ret = max(left_surface, right_surface);

    lnt mid_surface_heights = A[mid];
    ret = max(ret, mid_surface_heights * 1);

    int low = mid, high = mid;
    while (left <= low && high <= right) {
        if (left <= low - 1 && high + 1 <= right) {
            if (A[low - 1] < A[high + 1])
                mid_surface_heights = min(mid_surface_heights, A[++high]);
            else
                mid_surface_heights = min(mid_surface_heights, A[--low]);
        }
        else if (high + 1 <= right)
            mid_surface_heights = min(mid_surface_heights, A[++high]);
        else if (left <= low - 1)
            mid_surface_heights = min(mid_surface_heights, A[--low]);
        else
            break;

        ret = max(ret, mid_surface_heights * (high - low + 1));
    }

    return ret;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n;
    while (true) {
        cin >> n;

        if (n == 0)
            break;

        vector<lnt> A(n);
        for (lnt &e : A)
            cin >> e;

        cout << surface(A, 0, A.size() - 1) << endl;
    }
}
