#pragma once

int parents[500 + 1];   // 노드 번호는 1부터 시작.

int find_(int u) {
    if (u == parents[u]) return parents[u];
    else return parents[u] = find_(parents[u]);
}

void union_(int a, int b) {
    a = find_(a);
    b = find_(b);

    if (a == b)
        return;
    else if (a < b)
        parents[b] = a;
    else
        parents[a] = b;
}