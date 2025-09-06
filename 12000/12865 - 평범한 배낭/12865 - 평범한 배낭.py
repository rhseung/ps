# BOJ 12865 - 평범한 배낭
import sys
input = sys.stdin.readline

n: int
k: int
# DP: list[list[int]] = []
DP: list[int] = []
items: list[tuple[int, int]] = []

# def topdown(n: int, w: int) -> int:
#     if n < 0 or w < 0:
#         return 0
#     elif DP[n][w] != 0:
#         return DP[n][w]
#
#     selected = topdown(n - 1, w - items[n][0]) + items[n][1] if w >= items[n][0] else 0
#     unselected = topdown(n - 1, w)
#
#     DP[n][w] = max(selected, unselected)
#     return DP[n][w]

def main():
    global n, k, DP, items

    n, k = map(int, input().split())
    # DP = [[0 for _ in range(k + 1)] for _ in range(n)]
    DP = [0 for _ in range(k + 1)]
    items = [tuple(map(int, input().split())) for _ in range(n)]

    # print(topdown(n - 1, k))
    # print(DP)

    for w, v in items:
        for cur_w in range(k, w - 1, -1):   # 역순으로 해야 0/1 배낭이 가능
            DP[cur_w] = max(DP[cur_w], DP[cur_w - w] + v)

    print(DP[k])

if __name__ == "__main__":
    main()
