import sys

input = sys.stdin.readline

id_count = int(input())
require = int(input())
ids = list(map(int, input().split()))

ids.sort()
# idea. 양쪽 끝에서 시작
left, right = 0, len(ids) - 1
count = 0

# WC. left <= right 로 해서 WC 한 번 났음
#  - 예를 들어 require가 8인 경우, ids에 4가 있을 때, left와 right가 둘 다 같은 4를 가리키는 경우가 인정되기 때문
while left < right:
	key = ids[left] + ids[right]
	
	# idea. 수가 크면 좁아지고, 수가 크면 다음 스텝으로 스킵
	
	if key < require:
		left += 1
	elif key > require:
		right -= 1
	else:
		count += 1
		left += 1

print(count)
