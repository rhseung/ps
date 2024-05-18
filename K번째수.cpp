#include <string>
#include <vector>
#include <iostream>
#include <algorithm>

using namespace std;

vector<int> slice(vector<int> arr, int start, int end) {
    vector<int> ret;
    start--; end--;

    for(int i = 0; i < arr.size(); i++) {
        if (start <= i && i <= end) {
            ret.push_back(arr[i]);
        }
    }

    return ret;
}

vector<int> solution(vector<int> array, vector<vector<int>> commands) {
    vector<int> answer;
    vector<int> temp;

    for (int i = 0; i < commands.size(); i++) {
        temp = slice(array, commands[i][0], commands[i][1]);
        sort(temp.begin(), temp.end());
        answer.push_back(temp[commands[i][2] - 1]);
    }

    return answer;
}