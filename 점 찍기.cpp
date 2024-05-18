#include <string>
#include <vector>
#include <cmath>

using namespace std;

long long solution(int k, int d) {
    long long ret = 0;
    for (int x = 0; x <= d; x += k) {
        long long y = (long long)(std::sqrt((long long)d*d - (long long)x*x));
        ret += y / k + 1;
    }

    return ret;
}