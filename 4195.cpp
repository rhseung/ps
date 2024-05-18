#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

string find_(unordered_map<string, string> &S, string x) {
    if (x == S[x]) return x;
    else return S[x] = find_(S, S[x]);
}

void union_(unordered_map<string, string> &S, unordered_map<string, int> &nums, string a, string b) {
    a = find_(S, a);
    b = find_(S, b);

    if (a == b)
        return;
    else if (a < b) {
        S[b] = a;
        nums[a] += nums[b];     // b도 a를 루트로 갖도록 집합이 union 되었으니 집합 b의 개수를 집합 a에 더함.
    }
    else {
        S[a] = b;
        nums[b] += nums[a];
    }
}

void $() {
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int t;
    cin >> t;

    while (t--) {
        int f;
        cin >> f;

        unordered_map<string, string> names;
        unordered_map<string, int> nums;

        for (int i = 1; i <= f; ++i) {
            string s1, s2;
            cin >> s1 >> s2;

            if (names.find(s1) == names.end()) {
                names[s1] = s1;
                nums[s1] = 1;   // 친구 관계에는 자기도 포함되지 서로에게 추가되니까
            }
            if (names.find(s2) == names.end()) {
                names[s2] = s2;
                nums[s2] = 1;
            }

            union_(names, nums, s1, s2);
            cout << nums[find_(names, s1)] << endl;
        }
    }
}
