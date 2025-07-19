//
// Created by Hyunseung Ryu on 2025. 7. 19..
//

#ifndef BELLMAN_FORD_HPP
#define BELLMAN_FORD_HPP

#include <vector>
#define INF 0x3f3f3f3f

using namespace std;
typedef long long ll;

namespace graph {

/**
 * 벨만-포드 알고리즘. 다익스트라와 다르게 음의 가중치 간선이 있는 그래프에서도
 * 최단 경로를 찾을 수 있다.
 * @param edges 간선 리스트 (시작 정점 u, 끝 정점 v, 간선 가중치 w) 형태의
 * 튜플로 표현
 * @param vtx_count 정점 개수
 * @param start 시작 정점
 * @return 거리 배열과 음의 사이클 존재 여부
 */
inline pair<vector<int>, bool>
bellman_ford(const vector<tuple<int, int, int>> &edges, const int vtx_count,
             const int start) {
  vector dist(vtx_count + 1, INF);
  dist[start] = 0;

  for (int i = 0; i < vtx_count; ++i) { // 정점 개수만큼 루프 O(VE)
    for (auto [u, v, w] : edges) {
      if (dist[u] != INF &&
          dist[v] >
              dist[u] + w) // 검색된 적 없는 INF 노드로부터의 거리 계산은 제외
        dist[v] = dist[u] + w;
    }
  }

  bool has_cycle = false;
  for (auto [u, v, w] : edges) {
    if (dist[u] != INF &&
        dist[v] > dist[u] + w) { // 분명 모든 거리 계산을 끝냈는데도, 계속
                                 // dist가 감소 -> 음의 사이클 존재
      has_cycle = true;
      break;
    }
  }

  return {dist, has_cycle};
}

} // namespace graph

#endif // BELLMAN_FORD_HPP
