# 5582. [공통 부분 문자열](https://www.acmicpc.net/problem/5582)

| 티어 | 시간 제한 | 메모리 제한 | 제출 | 정답 | 맞힌 사람 | 정답 비율 |
|---|---|---|---:|---:|---:|---:|
| <img src="https://static.solved.ac/tier_small/11.svg" width="20px" /> | 2 초 | 256 MB | 23116 | 9673 | 7637 | 43.316% |

---

## 문제

두 문자열이 주어졌을 때, 두 문자열에 모두 포함된 가장 긴 공통 부분 문자열을 찾는 프로그램을 작성하시오.

어떤 문자열 s의 부분 문자열 t란, s에 t가 연속으로 나타나는 것을 말한다. 예를 들어, 문자열 
ABRACADABRA
의 부분 문자열은 
ABRA
, 
RAC
, 
D
, 
ACADABRA
, 
ABRACADABRA
, 빈 문자열 등이다. 하지만, 
ABRC
, 
RAA
, 
BA
, 
K
는 부분 문자열이 아니다.

두 문자열 
ABRACADABRA
와 
ECADADABRBCRDARA
의 공통 부분 문자열은 
CA
, 
CADA
, 
ADABR
, 빈 문자열 등이 있다. 이 중에서 가장 긴 공통 부분 문자열은 
ADABR
이며, 길이는 5이다. 또, 두 문자열이 
UPWJCIRUCAXIIRGL
와 
SBQNYBSBZDFNEV
인 경우에는 가장 긴 공통 부분 문자열은 빈 문자열이다.

## 입력

첫째 줄과 둘째 줄에 문자열이 주어진다. 문자열은 대문자로 구성되어 있으며, 길이는 1 이상 4000 이하이다.

## 출력

첫째 줄에 두 문자열에 모두 포함 된 부분 문자열 중 가장 긴 것의 길이를 출력한다.

## 예제

### 예제 입력 1

```
ABRACADABRA
ECADADABRBCRDARA
```

### 예제 출력 1

```
5
```

## 예제

### 예제 입력 2

```
UPWJCIRUCAXIIRGL
SBQNYBSBZDFNEV
```

### 예제 출력 2

```
0
```

## 출처

![image](https://licensebuttons.net/l/by-sa/4.0/88x31.png)

Olympiad
\> 
Japanese Olympiad in Informatics
\> 
JOI 2007/2008
2번

- 문제를 번역한 사람: baekjoon
- 문제의 오타를 찾은 사람: scka
- 데이터를 추가한 사람: eric00513

## 알고리즘 분류

- 다이나믹 프로그래밍
- 문자열
- 최장 공통 부분 수열 문제

