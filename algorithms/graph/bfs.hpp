//
// Created by Hyunseung Ryu on 2025. 7. 19..
//

#ifndef BFS_HPP
#define BFS_HPP

#include <iostream>
#include <queue>
#include <unordered_set>
#include <vector>

using namespace std;
typedef long long ll;

namespace graph {

/**
 * 너비 우선 탐색 (BFS)
 * @param adj 인접 리스트, [시작 정점: [...끝 정점들], ...] 형태.
 * @param start 시작 정점
 * @note 끝 정점들은 정렬되어 있어야 합니다.
 */
inline void bfs(const vector<vector<int>> &adj, const int start) {
  queue<int> queue;
  unordered_set<int> visited;

  queue.push(start);

  while (!queue.empty()) {
    const int vtx = queue.front();
    queue.pop();

    if (visited.contains(vtx))
      continue;
    visited.insert(vtx);

    // 방문한 정점 출력
    cout << vtx << " ";

    // 인접한 정점들을 순회, 정렬되어 있어야 함.
    for (const int u : adj[vtx]) {
      if (!visited.contains(u)) {
        queue.push(u);
      }
    }
  }
}

} // namespace graph

#endif // BFS_HPP
