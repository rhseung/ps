# BOJ 10999 - 구간 합 구하기 2

import sys
from array import array

# sys.setrecursionlimit(1 << 25)
input = sys.stdin.readline


class Node:
    __slots__ = ("sum", "lazy", "lch", "rch")

    def __init__(self):
        # 이 노드가 표현하는 구간에서의 "변화분" 합(초기 배열 대비)
        self.sum = 0
        # 아직 자식에게 전파되지 않은 구간 전체 덧셈 값(변화분)
        self.lazy = 0
        self.lch = None
        self.rch = None


def _push(node: Node, l: int, r: int) -> None:
    """ node.lazy를 자식에게 전파한다. """
    if node.lazy == 0 or l == r:
        return
    mid = (l + r) >> 1
    if node.lch is None:
        node.lch = Node()
    if node.rch is None:
        node.rch = Node()
    v = node.lazy
    node.lch.lazy += v
    node.rch.lazy += v
    node.lch.sum += v * (mid - l + 1)
    node.rch.sum += v * (r - mid)
    node.lazy = 0


def _update(node: Node, l: int, r: int, ql: int, qr: int, v: int) -> None:
    """ [ql, qr] 구간에 v를 더한다(변화분 누적). """
    if ql <= l and r <= qr:
        node.sum += v * (r - l + 1)
        node.lazy += v
        return
    _push(node, l, r)
    mid = (l + r) >> 1
    if ql <= mid:
        if node.lch is None:
            node.lch = Node()
        _update(node.lch, l, mid, ql, qr, v)
    if qr > mid:
        if node.rch is None:
            node.rch = Node()
        _update(node.rch, mid + 1, r, ql, qr, v)
    left_sum = node.lch.sum if node.lch else 0
    right_sum = node.rch.sum if node.rch else 0
    node.sum = left_sum + right_sum


def _query(node: Node | None, l: int, r: int, ql: int, qr: int) -> int:
    """ [ql, qr] 구간의 변화분 합을 구한다. """
    if node is None or qr < l or r < ql:
        return 0
    if ql <= l and r <= qr:
        return node.sum
    _push(node, l, r)
    mid = (l + r) >> 1
    s = 0
    if ql <= mid:
        s += _query(node.lch, l, mid, ql, qr)
    if qr > mid:
        s += _query(node.rch, mid + 1, r, ql, qr)
    return s


def main():
    # 입력: N(수의 개수), M(업데이트 수), K(합 쿼리 수)
    N, M, K = map(int, input().split())

    # 초기 배열 A[1..N]을 모두 읽어 prefix sum으로만 저장
    PS = array('q', [0])  # int64 prefix
    acc = 0
    for _ in range(N):
        acc += int(input())
        PS.append(acc)

    root = Node()
    total = M + K
    for _ in range(total):
        parts = input().split()
        a = int(parts[0])
        b = int(parts[1])
        c = int(parts[2])

        if b > c:
            b, c = c, b
        if a == 1:
            # 구간 [b, c]에 d 더하기
            d = int(parts[3])
            _update(root, 1, N, b, c, d)
        else:
            # 구간 합: (초기합) + (변화분합)
            base = PS[c] - PS[b - 1]
            delta = _query(root, 1, N, b, c)
            print(base + delta)


if __name__ == "__main__":
    main()
