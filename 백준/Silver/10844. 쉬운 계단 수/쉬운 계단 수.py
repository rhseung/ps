__problem__ = 'https://boj.kr/10844', '쉬운 계단 수'

import sys

input = sys.stdin.readline

n = int(input())

# 0    0    1    2    3    4    5    6    7    8    9    0  -> 12개
#          0 2  1 3  2 4  3 5  4 6  5 7  6 8  7 9  8
# 두 번째 자리 부터는 0이 올 수 있기 때문에 왼쪽 오른쪽 패딩은 별개로 하고 0~9도 써야함

D = [[0]*12 for _ in range(n)]
D[0][2:11] = [1] * 9    # base case

for i in range(1, n):
    for j in range(1, 11):
        # 9는 0과 10으로 계단 관계이나 10은 안되므로 조건 분기를 해줘도 되나,
        # 그냥 양쪽에 0을 padding하여 D[i-1][j+1] = 0으로 합을 무시할 수 있게 함
        D[i][j] = D[i - 1][j - 1] + D[i - 1][j + 1]

print(sum(D[n - 1]) % 1_000_000_000)
