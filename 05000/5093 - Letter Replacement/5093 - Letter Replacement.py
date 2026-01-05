# BOJ 5093 - Letter Replacement
import sys
from collections import defaultdict


def input() -> str: return sys.stdin.readline().rstrip()

mapping = ['*', '?', '/', '+', '!']

while (S := input()) != "#":
    freq = defaultdict(int)
    duplicates = []
    ret = ""

    for c in S:
        cl = c.lower()
        freq[cl] += 1
        if freq[cl] >= 2:
            if cl not in duplicates:
                duplicates.append(cl)
            ret += mapping[duplicates.index(cl)]
        else:
            ret += c

    print(ret)

