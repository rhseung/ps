import sys
from collections import deque
from dataclasses import dataclass

problem_name = "최솟값 찾기"
problem_url = "https://boj.kr/11003"
input = sys.stdin.readline

@dataclass
class Item:
	index: int
	value: int
	
	def __eq__(self, other):
		return isinstance(other, Item) \
			and self.index == other.index \
			and self.value == other.value
	
	def __repr__(self):
		return f"({self.index},{self.value})"
	
	__str__ = __repr__

length, delay = map(int, input().split())
numbers = list(map(int, input().split()))
deq: deque[Item] = deque()
minimums = []

# naive
# for i in range(length):
# 	minimums.append(min(numbers[max(0, i - delay + 1):i + 1]))

for i in range(length):
	# deq = deque([d for d in deq if not (d.value > numbers[i] or i - d.index >= delay)])
	# WC. 시간 초과
	#  어차피 크기 순으로 정렬될테니, 뒤에서부터 제거해도됨
	#  뒤에서부터 넣을 수보다 안 작아질 때까지 무한 pop이니까 이건 while이 더 맞음
	
	while len(deq) > 0 and deq[-1].value > numbers[i]:
		deq.pop()
	
	while len(deq) > 0 and i - deq[0].index >= delay:
		deq.popleft()

	# for j in range(len(deq) - 1, -1, -1):
	# 	if deq[j].value > numbers[i] or i - deq[j].index >= delay:
	# 		deq

	deq.append(Item(i, numbers[i]))
	minimums.append(deq[0].value)

for minimum in minimums:
	print(minimum, end=' ')
