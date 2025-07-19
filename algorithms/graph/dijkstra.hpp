//
// Created by Hyunseung Ryu on 2025. 7. 19..
//

#ifndef DIJKSTRA_HPP
#define DIJKSTRA_HPP

#include <queue>
#include <vector>
#define INF 0x3f3f3f3f

using namespace std;

namespace graph {

/**
 * 다익스트라 알고리즘
 * @param adj 인접 리스트, [시작 정점: [(가중치, 끝 정점), ...], ...] 형태.
 * @param start 시작 정점
 * @return 시작 정점으로부터 각 정점까지의 최단 거리 배열
 * @note 반드시 (가중치, 끝 정점)의 순서여야 합니다. 또한, 끝 정점들이 정렬되지
 * 않아도 됩니다. (우선순위 큐라 알아서)
 */
inline vector<int> dijkstra(const vector<vector<pair<int, int>>> &adj,
                            const int start) {
  priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>>
      priority_queue; // 이렇게 해야 값이 작을 수록 우선 순위를 갖는 최소 힙임
  vector dist(adj.size(), INF); // visited의 역할도 동시에 할 수 있음

  priority_queue.emplace(0, start);
  dist[start] = 0;

  while (!priority_queue.empty()) {
    auto [weight, vtx] = priority_queue.top();
    priority_queue.pop();

    if (weight > dist[vtx])
      continue; // 이미 최솟값보다 커진 이상 다음 경로를 탐색할 필요가 없음,
                // 가지치기

    for (auto [next_weight, next_vtx] : adj[vtx]) {
      if (dist[next_vtx] > dist[vtx] + next_weight) {
        dist[next_vtx] = dist[vtx] + next_weight;
        priority_queue.emplace(dist[next_vtx], next_vtx);
      }
    }
  }

  return dist;
}

} // namespace graph

#endif // DIJKSTRA_HPP
