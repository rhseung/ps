//
// Created by Hyunseung Ryu on 2025. 7. 19..
//

#ifndef BFS_HPP
#define BFS_HPP

#include <cassert>
#include <iostream>
#include <queue>
#include <unordered_set>
#include <vector>

using namespace std;
typedef long long ll;

namespace graph {

/**
 * 너비 우선 탐색 (BFS) - 인접 리스트
 * @param adj 인접 리스트, [시작 정점: [...끝 정점들], ...] 형태.
 * @param start 시작 정점
 * @param visit 방문한 정점을 처리하는 함수, 기본적으로 정점을 출력합니다.
 * @note 끝 정점들은 정렬되어 있어야 합니다.
 */
template <typename T> requires integral<T>
void bfs(const vector<vector<T>> &adj, const T start,
                const function<void(T)> &visit = [](const T v) { cout << v << " "; }) {
  queue<T> queue;
  unordered_set<T> visited;

  queue.push(start);

  while (!queue.empty()) {
    const T vtx = queue.front();
    queue.pop();

    if (visited.contains(vtx))
      continue;
    visited.insert(vtx);

    // 방문한 정점 출력
    visit(vtx);

    // 인접한 정점들을 순회, 정렬되어 있어야 함.
    for (const T u : adj[vtx]) {
      if (!visited.contains(u)) {
        queue.push(u);
      }
    }
  }
}

/**
 * 너비 우선 탐색 (BFS) - 인접 행렬
 * @param adj 인접 행렬, adj[i][j]가 true이면 i와 j가 연결되어 있음을 나타냅니다.
 * @param start 시작 정점
 * @param visit 방문한 정점을 처리하는 함수, 기본적으로 정점을 출력합니다.
 * @param reverse 인접 행렬을 역순으로 탐색할지 여부. true이면 인접한 정점들을 역순으로 탐색합니다.
 * @note 정점 번호를 오름차순(reverse가 true면 내림차순)으로 방문합니다.
 */
template <typename T> requires integral<T>
void bfs_matrix(const vector<vector<bool>> &adj, const T start,
                const function<void(T)> &visit = [](const T v) { cout << v << " "; }, const bool reverse = false) {
  assert(!adj.empty() && "Adjacency matrix must not be empty.");
  assert(adj.size() == adj[0].size() && "Adjacency matrix must be square.");

  queue<T> queue;
  unordered_set<T> visited;

  queue.push(start);

  while (!queue.empty()) {
    const T vtx = queue.front();
    queue.pop();

    if (visited.contains(vtx))
      continue;
    visited.insert(vtx);

    // 방문한 정점 출력
    visit(vtx);

    if (!reverse) {
      for (T u = 0; u < adj.size(); ++u) {
        if (adj[vtx][u] == true) {
          if (!visited.contains(u)) {
            queue.push(u);
          }
        }
      }
    } else {
      for (T u = adj.size() - 1; u >= 0; --u) {
        if (adj[vtx][u] == true) {
          if (!visited.contains(u)) {
            queue.push(u);
          }
        }
      }
    }
  }
}

} // namespace graph

#endif // BFS_HPP
