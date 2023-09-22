import sys
from dataclasses import dataclass

problem_url = "https://boj.kr/2493"
problem_name = "탑"
input = sys.stdin.readline

n = int(input())
heights = list(map(int, input().split()))

receives = [0 for _ in range(n)]

# naive
# for i in range(1, n):
# 	for front in range(i - 1, -1, -1):
# 		if heights[front] >= heights[i]:
# 			receives[i] = front + 1()
# 			break

@dataclass
class Item:
	idx: int
	value: int

stack: list[Item] = []
for i in range(n-1, -1, -1):
	new_item = Item(i, heights[i])
	
	while stack and new_item.value > stack[-1].value:
		top = stack.pop()
		receives[top.idx] = new_item.idx + 1    # 문제는 0~4가 아니라 1~5 인덱스임
	
	stack.append(new_item)

for e in receives:
	print(e, end=" ")
