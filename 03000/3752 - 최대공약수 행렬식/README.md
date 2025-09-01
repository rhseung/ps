# 3752. [최대공약수 행렬식](https://www.acmicpc.net/problem/3752)

| 티어                                                                  | 시간 제한 | 메모리 제한 | 제출 | 정답 | 맞힌 사람 | 정답 비율 |
| --------------------------------------------------------------------- | --------- | ----------- | ---: | ---: | --------: | --------: |
| <img src="https://static.solved.ac/tier_small/22.svg" width="20px" /> | 1 초      | 128 MB      |  493 |  247 |       204 |   53.543% |

---

## 문제

집합 S = {$x_{1}$
, $x_{2}$
, ..., $x_{n}$
}가 인수에 대해서 닫혀있으려면, 모든 $x_{i}$
∈ S에 대해서, $x_{i}$
의 모든 약수 d는 d ∈ S를 만족해야 한다.

인수에 대해 닫힌 집합 S를 최대공약수 행렬 (S) = ($s_{ij}$
), $s_{ij}$ = GCD($x_{i}$
,$x_{j}$
)로 만든 뒤, 이 행렬의 행렬식 (determinant)를 구하는 프로그램을 작성하시오.

\(D_n = \begin{vmatrix} \text{gcd}\left(x_1,x_1\right) & \text{gcd}\left(x_1,x_2\right) & \text{gcd}\left(x_1,x_3\right) & \dots & \text{gcd}\left(x_1,x_n\right) \\ \text{gcd}\left(x_2,x_1\right) & \text{gcd}\left(x_2,x_2\right) & \text{gcd}\left(x_2,x_3\right) & \dots & \text{gcd}\left(x_2,x_n\right) \\ \text{gcd}\left(x_3,x_1\right) & \text{gcd}\left(x_3,x_2\right) & \text{gcd}\left(x_3,x_3\right) & \dots & \text{gcd}\left(x_3,x_n\right) \\ \dots & \dots & \dots & \dots & \dots \\ \text{gcd}\left(x_n,x_1\right) & \text{gcd}\left(x_n,x_2\right) & \text{gcd}\left(x_n,x_3\right) & \dots & \text{gcd}\left(x_n,x_n\right) \\ \end{vmatrix}\)

## 입력

첫째 줄에 테스트 케이스의 개수 T가 주어진다. 각 테스트 케이스의 첫째 줄에는 집합 S의 원소 개수 n(0 < n < 1,000)이 주어진다.

다음 줄에는 집합의 원소 $x_{1}$
, $x_{2}$
, ..., $x_{n}$
이 주어진다. (0 < $x_{i}$
< 2\*$10^{9}$
, $x_{i}$
는 정수)

## 출력

각 테스트 케이스에 대해서 입력으로 주어진 집합 S의 최대공약수 행렬식을 1,000,000,007로 나눈 나머지를 출력한다.

## 예제

### 예제 입력 1

```
3
2
1 2
3
1 3 9
4
1 2 3 6
```

### 예제 출력 1

```
1
12
4
```

## 출처

ICPC
\>
Regionals
\>
Europe
\>
Southeastern European Regional Contest
\>
SEERC 2008
H번

- 문제를 번역한 사람: baekjoon

## 알고리즘 분류

- 수학
- 정수론
- 선형대수학
- 오일러 피 함수
