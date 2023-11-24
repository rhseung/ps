__problem__ = 'https://boj.kr/1931', '회의실 배정'

import sys

input = sys.stdin.readline

n = int(input().strip())
M = [tuple(map(int, input().split())) for _ in range(n)]    # (시작 시간, 종료 시간)

M.sort(key=lambda x: (x[1], x[0]))

count = 1   # 가능한 회의 개수
end = M[0][1]   # 첫 번째 회의의 종료 시간

for i in range(1, n):
    if end <= M[i][0]:
        end = M[i][1]
        count += 1

print(count)
