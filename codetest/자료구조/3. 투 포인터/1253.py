import sys

problem_name = "좋다"
problem_url = "https://boj.kr/1253"
input = sys.stdin.readline

length = int(input())
numbers = list(map(int, input().split()))

numbers.sort()

# AC. 생각보다 쉽게 풀려서 당황함
#  - 리스트의 모든 요소를 순회하면서 그 요소를 제외한 리스트에서 1940번을 수행하면 일단 느려도 되겠지 했는데 진짜 AC뜸

count = 0
for i in range(len(numbers)):
	except_numbers = numbers[:i] + numbers[i+1:]
	number = numbers[i]
	left, right = 0, len(except_numbers) - 1
	
	while left < right:
		key = except_numbers[left] + except_numbers[right]
		
		if key > number:
			right -= 1
		elif key < number:
			left += 1
		else:
			count += 1
			break
		
print(count)
