//
// Created by Hyunseung Ryu on 2025. 9. 6..
//

#include <iostream>
using namespace std;

int fibonacci(int n) {
    if (n == 1) return 1;
    if (n == 2) return 1;

    cout << "fibonacci(" << n << ") called" << endl;

    return fibonacci(n - 1) + fibonacci(n - 2);
}

// int F[1000] = { 0, 1, 1, };
//
// int fibonacci(int n) {
//     if (n == 1) return 1;
//     if (n == 2) return 1;
//
//     if (F[n] != 0)
//         return F[n];
//
//     cout << "fibonacci(" << n << ") called" << endl;
//
//     return F[n] = fibonacci(n - 1) + fibonacci(n - 2);
// }

int main() {
    cout << fibonacci(10) << endl;

    return 0;
}