#include <vector>
#include <iostream>
using namespace std;

#define endl "\n"
#define SIZE 50001

bool sieve[SIZE];
// sieve[3] = false: 3이 소수다

int solution(vector<int> nums) {
    sieve[0] = true;
    sieve[1] = true;

    for (int i = 2; i <= SIZE; ++i) {
        if (sieve[i] == true)
            continue;

        int k = 2;
        while (i * k <= SIZE) {
            sieve[i * k] = true;
            k++;
        }
    }

    int cnt = 0;

    for (int i = 0; i < nums.size() - 2; ++i) {
        for (int j = i + 1; j < nums.size() - 1; ++j) {
            for (int k = j + 1; k < nums.size(); ++k) {
                if (sieve[nums[i] + nums[j] + nums[k]] == false)
                    cnt++;
            }
        }
    }

    return cnt;
}