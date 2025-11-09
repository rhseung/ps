# BOJ 22864 - 피로도
import sys
def input() -> str: return sys.stdin.readline()

a, b, c, m = map(int, input().split())

work = 0
fatigue = 0
hour = 0

while hour < 24:
    if fatigue + a > m:    # rest
        hour += 1
        fatigue = max(fatigue - c , 0)
    else:   # work
        hour += 1
        fatigue += a
        work += b

print(work)