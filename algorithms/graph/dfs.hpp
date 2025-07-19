//
// Created by Hyunseung Ryu on 2025. 7. 19..
//

#ifndef DFS_HPP
#define DFS_HPP

#include <iostream>
#include <ranges>
#include <unordered_set>
#include <vector>

using namespace std;

namespace graph {

/**
 * 깊이 우선 탐색 (DFS) - 재귀적 구현
 * @param adj 인접 리스트, [시작 정점: [...끝 정점들], ...] 형태.
 * @param vtx 현재 방문할 정점
 * @param visited 방문한 정점 집합
 * @note 끝 정점들은 정렬되어 있어야 합니다.
 */
inline void dfs_recursive(const vector<vector<int>> &adj, const int vtx,
                          unordered_set<int> &visited) {
  visited.insert(vtx);

  // 방문한 정점 출력
  cout << vtx << " ";

  for (const int u : adj[vtx]) {
    if (!visited.contains(u)) {
      dfs_recursive(adj, u, visited);
    }
  }
}

/**
 * 깊이 우선 탐색 (DFS) - 스택을 이용한 반복적 구현
 * @param adj 인접 리스트, [시작 정점: [...끝 정점들], ...] 형태.
 * @param start 시작 정점
 * @note 끝 정점들은 정렬되어 있어야 합니다.
 */
inline void dfs(const vector<vector<int>> &adj, const int start) {
  stack<int> stack;
  unordered_set<int> visited;

  stack.push(start);

  while (!stack.empty()) {
    const int vtx = stack.top();
    stack.pop();

    if (visited.contains(vtx))
      continue;
    visited.insert(vtx);

    // 방문한 정점 출력
    cout << vtx << " ";

    for (const int u : ranges::reverse_view(adj[vtx])) {
      if (!visited.contains(u)) {
        stack.push(u);
      }
    }
  }
}

} // namespace graph

#endif // DFS_HPP
