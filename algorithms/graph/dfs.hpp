//
// Created by Hyunseung Ryu on 2025. 7. 19..
//

#ifndef DFS_HPP
#define DFS_HPP

#include <assert.h>
#include <iostream>
#include <ranges>
#include <unordered_set>
#include <vector>

using namespace std;

namespace graph {

/**
 * 깊이 우선 탐색 (DFS) - 재귀적 구현, 인접 리스트
 * @param adj 인접 리스트, [시작 정점: [...끝 정점들], ...] 형태.
 * @param vtx 현재 방문할 정점
 * @param visited 방문한 정점 집합
 * @param visit 방문한 정점을 처리하는 함수, 기본적으로 정점을 출력합니다.
 * @note 끝 정점들은 정렬되어 있어야 합니다.
 */
template <typename T> requires integral<T>
void dfs(const vector<vector<T>> &adj, const T vtx,
                          unordered_set<T> &visited, const function<void(T)> &visit = [](const T v) { cout << v << " "; }) {
  visited.insert(vtx);

  // 방문한 정점 출력
  visit(vtx);

  for (const T u : adj[vtx]) {
    if (!visited.contains(u)) {
      dfs(adj, u, visited);
    }
  }
}

/**
 * 깊이 우선 탐색 (DFS) - 스택을 이용한 반복적 구현, 인접 리스트
 * @param adj 인접 리스트, [시작 정점: [...끝 정점들], ...] 형태.
 * @param start 시작 정점
 * @param visit 방문한 정점을 처리하는 함수, 기본적으로 정점을 출력합니다.
 * @note 끝 정점들은 정렬되어 있어야 합니다.
 */
template <typename T> requires integral<T>
void dfs(const vector<vector<T>> &adj, const T start, const function<void(T)> &visit = [](const T v) { cout << v << " "; }) {
  stack<T> stack;
  unordered_set<T> visited;

  stack.push(start);

  while (!stack.empty()) {
    const T vtx = stack.top();
    stack.pop();

    if (visited.contains(vtx))
      continue;
    visited.insert(vtx);

    // 방문한 정점 출력
    visit(vtx);

    for (const T u : ranges::reverse_view(adj[vtx])) {
      if (!visited.contains(u)) {
        stack.push(u);
      }
    }
  }
}

/**
 * 깊이 우선 탐색 (DFS) - 재귀적 구현, 인접 행렬
 * @param adj 인접 행렬, adj[i][j]의 true/false 여부로 연결 여부를 나타냅니다.
 * @param vtx 현재 방문할 정점
 * @param visited 방문한 정점 집합
 * @param visit 방문한 정점을 처리하는 함수, 기본적으로 정점을 출력합니다.
 * @param reverse 인접 행렬을 역순으로 탐색할지 여부. true이면 인접한 정점들을 역순으로 탐색합니다.
 * @note 정점 번호를 오름차순(reverse가 true면 내림차순)으로 방문합니다.
 */
template <typename T> requires integral<T>
void dfs_matrix(const vector<vector<bool>> &adj, const T vtx,
                          unordered_set<T> &visited, const function<void(T)> &visit = [](const T v) { cout << v << " "; }, const bool reverse = false) {
  assert(!adj.empty() && "Adjacency matrix must not be empty.");
  assert(adj.size() == adj[0].size() && "Adjacency matrix must be square.");

  visited.insert(vtx);

  // 방문한 정점 출력
  visit(vtx);

  if (!reverse) {
    for (T w = 0; w < adj.size(); ++w) {
      if (adj[vtx][w] == true) {
        if (!visited.contains(w)) {
          dfs_matrix(adj, w, visited);
        }
      }
    }
  } else {
    for (T w = adj.size() - 1; w >= 0; --w) {
      if (adj[vtx][w] == true) {
        if (!visited.contains(w)) {
          dfs_matrix(adj, w, visited);
        }
      }
    }
  }
}

/**
 * 깊이 우선 탐색 (DFS) - 스택을 이용한 반복적 구현, 인접 행렬
 * @param adj 인접 행렬, adj[i][j]의 true/false 여부로 연결 여부를 나타냅니다.
 * @param start 시작 정점
 * @param visit 방문한 정점을 처리하는 함수, 기본적으로 정점을 출력합니다.
 * @param reverse 인접 행렬을 역순으로 탐색할지 여부. true이면 인접한 정점들을 역순으로 탐색합니다.
 * @note 정점 번호를 오름차순(reverse가 true일 경우 내림차순)으로 방문합니다.
 */
template <typename T> requires integral<T>
void dfs_matrix(const vector<vector<bool>> &adj, const T start, const function<void(T)> &visit = [](const T v) { cout << v << " "; }, const bool reverse = false) {
  assert(!adj.empty() && "Adjacency matrix must not be empty.");
  assert(adj.size() == adj[0].size() && "Adjacency matrix must be square.");

  stack<T> stack;
  unordered_set<T> visited;

  stack.push(start);

  while (!stack.empty()) {
    const T vtx = stack.top();
    stack.pop();

    if (visited.contains(vtx))
      continue;
    visited.insert(vtx);

    // 방문한 정점 출력
    visit(vtx);

    if (!reverse) {
      for (T w = adj.size() - 1; w >= 0; --w) {
        if (adj[vtx][w] == true) {
          if (!visited.contains(w)) {
            stack.push(w);
          }
        }
      }
    } else {
      for (T w = 0; w < adj.size(); ++w) {
        if (adj[vtx][w] == true) {
          if (!visited.contains(w)) {
            stack.push(w);
          }
        }
      }
    }
  }
}

} // namespace graph

#endif // DFS_HPP
