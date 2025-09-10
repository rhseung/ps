# 8291. [Coprime Numbers](https://www.acmicpc.net/problem/8291)

| 티어 | 시간 제한 | 메모리 제한 | 제출 | 정답 | 맞힌 사람 | 정답 비율 |
|---|---|---|---:|---:|---:|---:|
| <img src="https://static.solved.ac/tier_small/19.svg" width="20px" /> | 5 초 | 128 MB | 301 | 139 | 110 | 47.210% |

---

## 문제

Two positive integers are said to be coprime if 1 is their only common divisor. Given a sequence of positive integers $a_{1}$
, $a_{2}$
, ..., $a_{n}$
, find the number of pairs of its terms which are coprime.

## 입력

The first line of input contains one integer n (1 ≤ n ≤ 1,000,000) denoting the length of the sequence. The second line contains n integers $a_{i}$
(1 ≤ $a_{i}$
≤ 3,000,000).

## 출력

Your program should output one integer representing the number of pairs (i, j) such that 1 ≤ i < j ≤ n and $a_{i}$
is coprime with $a_{j}$
.

## 예제

### 예제 입력 1

```
5
3 6 4 7 3
```

### 예제 출력 1

```
6
```

## 출처

Contest
\> 
Algorithmic Engagements
\> 
PA 2011
7-5번

- 데이터를 추가한 사람: h0ngjun7

## 알고리즘 분류

- 포함 배제의 원리
- 수학
- 정수론

