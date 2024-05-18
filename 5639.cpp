#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

typedef struct BTNode {
    int data{};
    struct BTNode *left = nullptr;
    struct BTNode *right = nullptr;

    bool leaf() {
        return left == nullptr && right == nullptr;
    }
} BTNode;

int A[10000];

void f(int s, int e) {
    if (s > e)
        return;

    int root = A[s];

    int p = e + 1;
    for (int i = s + 1; i <= e; ++i) {
        if (A[i] > root) {
            p = i;
            break;
        }
    }

    f(s + 1, p - 1);
    f(p, e);

    cout << root << endl;
}

void solution() {
    int i = 0;
    while (cin >> A[i++]) {}

    f(0, i - 2);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solution();
    return 0;
}
