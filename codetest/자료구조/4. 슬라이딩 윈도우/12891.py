import sys

problem_name = "DNA 비밀번호"
problem_url = "https://boj.kr/12891"
input = sys.stdin.readline

length, part_length = map(int, input().split())
dna_str = input().strip()
min_A, min_C, min_G, min_T = map(int, input().split())

count = 0
min_limit = {'A': min_A, 'C': min_C, 'G': min_G, 'T': min_T}
end = part_length

part = dna_str[end - part_length:end]
freq = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
for c in part:
	freq[c] += 1

# WC. 한 번 WC 났었는데,
#  그 이유가 무지성으로 윈도우 슬라이딩하면서 `part_length` 길이의 문자열을 또 for 돌려서
#  빈도를 셌었는데 그게 너무 느려서 시간 초과남

# AC. 그래서 맨 처음에만 4개 세고, 그 다음은 슬라이딩 할 때 바뀌는 맨 앞과 맨 뒤의 빈도만 조절했더니 AC뜸

while True:
	if all(freq[k] >= min_limit[k] for k in freq):
		# print(dna_str[end - part_length:end])
		count += 1
	
	if end == length:
		break
	
	freq[dna_str[end - part_length]] -= 1
	freq[dna_str[end]] += 1
	end += 1

print(count)
