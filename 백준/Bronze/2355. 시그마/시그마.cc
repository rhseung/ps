#include <iostream>
using namespace std;
using lnt = long long int;

lnt sum(int a, int b) {
    return ((lnt)a + b)*((lnt)b - a + 1)/2;
}

int main() {
    int a, b;
    cin >> a >> b;
    
    if (a > b) {
        int tmp = a;
        a = b;
        b = tmp;
    }
    
    if (a < 0 && 0 < b) {
        cout << (sum(a, 0) + sum(0, b));
    } else {
        cout << sum(a, b);
    }
    
    return 0;
}