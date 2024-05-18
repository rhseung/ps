#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using lnt = long long int;

int surface(vector<int> &A, int left, int right) {
    if (left == right)
        return A[left];

    int mid = (left + right) / 2;
    int left_surface = surface(A, left, mid);
    int right_surface = surface(A, mid + 1, right);
    int ret = max(left_surface, right_surface);

    int mid_surface_heights = A[mid];
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
    cin >> n;

    vector<int> A(n);
    for (int &e : A)
        cin >> e;

    cout << surface(A, 0, A.size() - 1);
}
