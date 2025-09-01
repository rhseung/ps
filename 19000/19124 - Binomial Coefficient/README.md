# 19124. [Binomial Coefficient](https://www.acmicpc.net/problem/19124)

| 티어                                                                  | 시간 제한 | 메모리 제한 | 제출 | 정답 | 맞힌 사람 | 정답 비율 |
| --------------------------------------------------------------------- | --------- | ----------- | ---: | ---: | --------: | --------: |
| <img src="https://static.solved.ac/tier_small/21.svg" width="20px" /> | 2 초      | 512 MB      |  171 |  108 |        42 |   60.000% |

---

## 문제

Given $n, k$, calculate $\binom{n}{k} = \frac{n!}{k!(n - k)!} \bmod ($2^{32}$)$.

## 입력

$2$ integers $n, k$ ($1 \leq n \leq $10^{18}$, 0 \leq k \leq n$).

## 출력

A single integer denotes the value.

## 예제

### 예제 입력 1

```
4 2
```

### 예제 출력 1

```
6
```

## 예제

### 예제 입력 2

```
1000000000 500000000
```

### 예제 출력 2

```
4209467392
```

## 출처

Camp
\>
Petrozavodsk Programming Camp
\>
Winter 2015
\>
Day 1: Xiaoxu Guo Contest 3
A번

## 알고리즘 분류

- 수학
- 정수론
