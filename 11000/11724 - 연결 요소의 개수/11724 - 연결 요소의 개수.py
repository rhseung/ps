import sys

problem_url = "https://boj.kr/11724"
problem_name = "연결 요소의 개수"
input = sys.stdin.readline

v, e = map(int, input().split())

graph = [[] for _ in range(v + 1)]    # 0 고려
for _ in range(e):
	start, end = map(int, input().split())
	graph[start].append(end)
	graph[end].append(start)

def dfs(graph, now, visited):
	visited[now] = True
	
	for w in graph[now]:
		if not visited[w]:
			dfs(graph, w, visited)

# 연결 요소의 개수 = 서로 동떨어져 있는 그래프의 개수
# 1을 dfs로 넘기면 1과 연결된 모든 요소의 visit을 전부 True로 바꾸게 된다
# 모든 정점에 대해 dfs를 넘길 때 그 정점이 dfs를 전에서 다 돌리고도 visit이 False라서 넘어갈 수 있다는 건 곧 동떨어진 그래프라는 뜻

count = 0
visited = [False] * len(graph)
for i in range(1, v + 1):
	if not visited[i]:
		count += 1
		dfs(graph, i, visited)

print(count)
