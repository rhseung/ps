# 1806. [부분합](https://www.acmicpc.net/problem/1806)

| 티어 | 시간 제한 | 메모리 제한 | 제출 | 정답 | 맞힌 사람 | 정답 비율 |
|---|---|---|---:|---:|---:|---:|
| <img src="https://static.solved.ac/tier_small/12.svg" width="50%" /> | 0.5 초  (하단 참고) | 128 MB | 129843 | 37048 | 26188 | 26.799% |

---

## 문제

10,000 이하의 자연수로 이루어진 길이 N짜리 수열이 주어진다. 이 수열에서 연속된 수들의 부분합 중에 그 합이 S 이상이 되는 것 중, 가장 짧은 것의 길이를 구하는 프로그램을 작성하시오.

## 입력

첫째 줄에 N (10 ≤ N < 100,000)과 S (0 < S ≤ 100,000,000)가 주어진다. 둘째 줄에는 수열이 주어진다. 수열의 각 원소는 공백으로 구분되어져 있으며, 10,000이하의 자연수이다.

## 출력

첫째 줄에 구하고자 하는 최소의 길이를 출력한다. 만일 그러한 합을 만드는 것이 불가능하다면 0을 출력하면 된다.

## 예제

### 예제 입력 1

```
10 15
5 1 3 5 10 7 4 9 2 8
```

### 예제 출력 1

```
2
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
SEERC 2006
B번

- 문제를 번역한 사람: author5
- 시간 제한을 수정한 사람: cheetose
- 잘못된 데이터를 찾은 사람: corhydrae
- 잘못된 조건을 찾은 사람: isku
- 데이터를 추가한 사람: kiwiyou , leeingyun96 , ppqhdl2 , stresstalmo , wookje , YunGoon
- 빠진 조건을 찾은 사람: rlarlghks970113
- 문제의 오타를 찾은 사람: ZZangZZang

## 시간 제한

- Java 8: 1 초
- Java 8 (OpenJDK): 1 초
- Java 11: 1 초
- Kotlin (JVM): 1 초
- Java 15: 1 초

## 알고리즘 분류

- 누적 합
- 두 포인터

