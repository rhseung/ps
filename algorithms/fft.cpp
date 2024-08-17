#include <vector>
#include <complex>
#include <cmath>

int n = 10;
vector<complex> A(n), B(n);

void DFT(vector<complex> &A, vector<complex> &B, int n) {
    int N = 1<<ceil(log2(n));
    
}

vector<complex> dot(vector<complex> &A, vector<complex> &B, int n) {
    vector<complex> ret(n);
    for (int i = 0; i < n; ++i)
        ret[i] = A[i] * B[i];

    return ret;
}

void IDFT(vector<complex> &A, vector<complex> &B) {

}