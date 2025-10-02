# BOJ 2096 - 내려가기
import sys
def input() -> str: return sys.stdin.readline()

n = int(input())
initial = 0, 1_000_000

a, b, c = map(int, input().split())
DP_before = [(a, a), (b, b), (c, c)]
DP_after = [initial for _ in range(3)]

for line in range(1, n):
    L = list(map(int, input().split()))

    for cur in range(3):
        last_curs = list(filter(lambda x: 0 <= x < 3, [cur - 1, cur, cur + 1]))
        max_v, min_v = initial

        for last_cur in last_curs:
            max_, min_ = DP_before[last_cur]
            max_v = max(max_v, max_ + L[cur])
            min_v = min(min_v, min_ + L[cur])

        DP_after[cur] = max_v, min_v

    DP_before = DP_after
    DP_after = [initial for _ in range(3)]

maxs, mins = zip(*DP_before)
print(max(maxs), min(mins))