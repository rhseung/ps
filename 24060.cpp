#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

int k;
int *A, *tmp;
int cnt = 0, result = -1;

void merge(int p, int q, int r) {
    int i = p, j = q + 1, t = 1;

    while (i <= q && j <= r) {
        if (A[i] <= A[j])
            tmp[t++] = A[i++];
        else
            tmp[t++] = A[j++];
    }

    while (i <= q)
        tmp[t++] = A[i++];

    while (j <= r)
        tmp[t++] = A[j++];

    i = p, t = 1;
    while (i <= r) {
        int v = tmp[t++];
        A[i++] = v;

        cnt++;
        if (cnt == k) {
            result = v;
            break;
        }
    }
}

void merge_sort(int p, int r) {
    if (p < r) {
        int q = (p + r) / 2;
        merge_sort(p, q);
        merge_sort(q + 1, r);
        merge(p, q, r);
    }
}

void solution() {
    int l;
    cin >> l >> k;

    A = new int[l];
    tmp = new int[l];
    for (int i = 0; i < l; ++i)
        cin >> A[i];

    merge_sort(0, l - 1);
    cout << result;

    delete A;
    delete tmp;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
