# 20226. [Luggage](https://www.acmicpc.net/problem/20226)

| 티어                                                                  | 시간 제한              | 메모리 제한 | 제출 | 정답 | 맞힌 사람 | 정답 비율 |
| --------------------------------------------------------------------- | ---------------------- | ----------- | ---: | ---: | --------: | --------: |
| <img src="https://static.solved.ac/tier_small/22.svg" width="20px" /> | 10 초 (추가 시간 없음) | 512 MB      |  755 |  211 |       105 |   22.976% |

---

## 문제

Mr. Yokohama is estimating the delivery fare for a number of luggage pieces. The fare for a piece is determined by its width _w_ , depth _d_ and height _h_ , each rounded up to an integer. The fare is proportional to the _sum_ of them.

![image](https://upload.acmicpc.net/e63dd384-ee2c-4c25-b294-00483c12a2c7/-/preview/)

The list of the luggage pieces is at hand, but the list has the _product_ _w_ × _d_ × _h_ for each piece, instead of the _sum_ _w_ + _d_ + _h_ by mistake. This information is not enough to calculate the exact delivery fare.

Mr. Yokohama therefore decided to estimate the minimum possible delivery fare. To this end, given the listed _product_ _p_ for each of the luggage pieces, the minimum possible _sum_ _s_ = _w_ + _d_ + _h_ satisfying _p_ = _w_ × _d_ × _h_ should be found.

You are requested to help Mr. Yokohama by writing a program that, when given the product _p_ , computes the minimum sum _s._

## 입력

The input consists of multiple datasets. Each of the datasets has one line containing an integer _p_ (0 < _p_ < $10^{15}$
).

The end of the input is indicated by a line containing a zero.

The number of datasets does not exceed 300.

## 출력

For each dataset, output a single line containing an integer _s_ . _s_ should be the minimum possible sum _w_ + _d_ + _h_ of three positive integers, _w,_ _d,_ and _h,_ satisfying _p_ = _w_ × _d_ × _h._

## 예제

### 예제 입력 1

```
1
2
6
8
729
47045881
12137858827249
562949953421312
986387345919360
999730024299271
999998765536093
0
```

### 예제 출력 1

```
3
4
6
6
27
1083
6967887
262144
298633
299973
999998765536095
```

## 출처

ICPC
\>
Regionals
\>
Asia Pacific
\>
Japan
\>
Japan Domestic Contest
\>
2020 Japan Domestic Contest
C번

## 알고리즘 분류

- 수학
- 정수론
- 이분 탐색
- 소수 판정
- 소인수분해
- 폴라드 로
- 밀러–라빈 소수 판별법
