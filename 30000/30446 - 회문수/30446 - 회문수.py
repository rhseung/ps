# BOJ 30446 - 회문수
import sys
def input() -> str: return sys.stdin.readline().rstrip()

s = input().strip()
n = int(s)
l = len(s)

# 100000~999999 이하의 회문수 개수 = ___/___ 앞의 3개만 결정하면 됨 -> 9 * 10 * 10 = 900개
# 100000~123456 이하의 회문수 개수 = 123456 > 123321이므로 100___ ~ 123___ 까지 24개

cnt = 0
for length in range(1, l):
    half_len = (length + 1) // 2
    cnt += 9 * 10 ** (half_len - 1)

half_len = (l + 1) // 2
prefix = int(s[:half_len])
base = 10 ** (half_len - 1)

p_str = str(prefix)
if l % 2 == 0:
    cand = int(p_str + p_str[::-1])
else:
    cand = int(p_str + p_str[-2::-1])
# print(f"{p_str=}, {cand=}, {n=}, {prefix=}, {base=}")

if cand <= n:
    cnt += (prefix - base + 1)
else:
    cnt += (prefix - base)

print(cnt)