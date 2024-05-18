#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

#define SIZE 100'000
int inorder_index[SIZE];      // LVR
int postorder[SIZE];        // LRV
int n;

void get_preorder(int plow, int phigh, int ilow, int ihigh) {
    if (plow <= phigh && ilow <= ihigh) {
        int oper = postorder[phigh];
        int oper_index_inorder = inorder_index[oper];

        cout << oper << " ";
        int left_length = oper_index_inorder - ilow;
        int right_length = ihigh - oper_index_inorder;

        get_preorder(plow, plow + left_length - 1, ilow, oper_index_inorder - 1);
        get_preorder(plow + left_length, phigh - 1, oper_index_inorder + 1, ihigh);
    }
}

/**
     1
   2   3
  4 5 6 7

[4 2 5] (1) [6 3 7]
[4 5 {2}] [6 7 3] (1)

1 2 4 5 3 6 7
 */

void solution() {
    cin >> n;

    for (int i = 0; i < n; ++i) {
        int tmp;
        cin >> tmp;
        inorder_index[tmp] = i;
    }
    for (int i = 0; i < n; ++i)
        cin >> postorder[i];

    get_preorder(0, n - 1, 0, n - 1);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
