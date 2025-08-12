// BOJ 20226 - Luggage
#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

inline ull modmul(const ull a, const ull b, const ull M) {
    const ll ret = a * b - M * static_cast<ull>(1.L / M * a * b);
    return ret + M * (ret < 0) - M * (ret >= static_cast<ll>(M));
}

inline ull modpow(ull b, ull e, const ull M) {
    ull ans = 1;
    for (; e; b = modmul(b, b, M), e /= 2)
        if (e & 1) ans = modmul(ans, b, M);
    return ans;
}

/**
   * 확률적 소수 판별 함수, 7*10^18 까지 정확도 보장
   * O(k log n) (k는 테스트 횟수, 일반적으로 7)
   * Miller-Rabin 알고리즘을 사용합니다.
   * @param n
   * @return n이 소수이면 true, 아니면 false
   */
inline bool is_prime_fast(const ull n) {
    if (n < 2 || n % 6 % 4 != 1) return (n | 1) == 3;
    const ull s = __builtin_ctzll(n - 1);
    const ull d = n >> s;

    for (const ull a : {2, 325, 9375, 28178, 450775, 9780504, 1795265022}) {
        ull p = modpow(a % n, d, n);
        ull i = s;

        while (p != 1 && p != n - 1 && a % n && i--)
            p = modmul(p, p, n);

        if (p != n - 1 && i != s)
            return false;
    }

    return true;
}

/**
     * Pollard's rho 알고리즘을 사용하여 n의 소인수 중 하나를 찾습니다.
     * 이 알고리즘은 n이 합성수일 때 작동하며, n이 소수일 경우에는 실패할 수 있습니다.
     * 따라서 이 함수를 사용하기 전에 `is_prime_fast` 함수를 사용하여 n이 소수인지 확인하는 것이 좋습니다.
     * @param n
     * @return n의 1도 아니고 n도 아닌 소인수 중 하나
     */
inline ull pollard(const ull n) {
    ull x = 0, y = 0, t = 30, prd = 2, i = 1, q;
    auto f = [&](const ull x_) {
        return modmul(x_, x_, n) + i;
    };

    while (t++ % 40 || __gcd(prd, n) == 1) {
        if (x == y) x = ++i, y = f(x);
        if ((q = modmul(prd, max(x, y) - min(x, y), n))) prd = q;
        x = f(x), y = f(f(y));
    }

    return __gcd(prd, n);
}

/**
 * n의 소인수를 찾습니다.
 * 이 함수는 Pollard's rho 알고리즘을 사용하여 n의 소인수 중 하나를 찾고,
 * 재귀적으로 나머지 소인수를 찾습니다
 * @param n
 * @return n의 소인수들의 벡터 (정렬되어 있지 않습니다)
 */
inline vector<ull> factor(const ull n) {
    if (n <= 1) return {};
    if (is_prime_fast(n)) return {n};

    const ull x = pollard(n);
    auto l = factor(x), r = factor(n / x);
    l.insert(l.end(), r.begin(), r.end());

    return l;
}

/**
 * n의 소인수와 그 개수를 맵 형태로 반환합니다.
 * 예를 들어, n = 12이면 {2: 2, 3: 1}을 반환합니다.
 * 이 함수는 `factor` 함수를 사용하여 n의 소인수를 찾고,
 * 각 소인수의 개수를 세어 맵에 저장합니다.
 * @param n
 * @return n의 소인수와 그 개수를 저장한 맵
 */
inline map<ull, ull> factor_map(const ull n) {
    map<ull, ull> ret;
    for (const ull f : factor(n)) {
        if (!ret.contains(f))
            ret[f] = 0;
        ret[f]++;
    }

    return ret;
}

/**
 * n의 소인수와 그 개수를 쌍(pair) 형태로 반환합니다.
 * 예를 들어, n = 12이면 {(2, 2), (3, 1)}을 반환합니다.
 * 이 함수는 `factor_map` 함수를 사용하여 n의 소인수를 찾고,
 * 각 소인수와 그 개수를 쌍(pair)으로 만들어 벡터에 저장합니다.
 * @param n
 * @return n의 소인수와 그 개수를 저장한 벡터
 */
inline vector<pair<ull, ull>> factor_pair(const ull n) {
    vector<pair<ull, ull>> ret;
    for (const auto& [factor, count] : factor_map(n)) {
        ret.emplace_back(factor, count);
    }
    return ret;
}

// dfs를 이용한 약수 구하기
void dfs(const size_t idx, const ull cur, const vector<pair<ull, ull>>& factor_pair, vector<ull>& divisors) {
    if (idx == factor_pair.size()) {
        divisors.push_back(cur);
        return;
    }

    const auto& [factor, count] = factor_pair[idx];
    for (ull i = 0, f = 1; i <= count; ++i) {
        dfs(idx + 1, cur * f, factor_pair, divisors);
        f *= factor;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    ull p;
    while (true) {
        cin >> p;
        if (p == 0)
            break;

        const auto factor_pairs = factor_pair(p);
        vector<ull> divisors; // 약수
        dfs(0, 1, factor_pairs, divisors);
        ranges::sort(divisors);

        ull ret = 1e18;
        for (int i = 0; i < divisors.size(); ++i) {
            const ull d = p / divisors[i];
            const ull x = divisors[i];
            const ull opt = ceil(2.0 * sqrt(static_cast<long double>(x)));
            if (opt + d > ret)
                break;

            const int idx = lower_bound(divisors.begin(), divisors.end(), static_cast<ull>(sqrt(static_cast<long double>(x)))) - divisors.
                begin();
            int diff = 0;

            while (idx - diff >= 0 || idx + diff < divisors.size()) {
                bool flag = false;
                if (idx - diff >= 0 && x % divisors[idx - diff] == 0) {
                    const ull w = divisors[idx - diff];
                    const ull h = x / w;
                    ret = min(ret, w + h + d);
                    flag = true;
                }
                if (idx + diff < divisors.size() && x % divisors[idx + diff] == 0) {
                    const ull w = divisors[idx + diff];
                    const ull h = x / w;
                    ret = min(ret, w + h + d);
                    flag = true;
                }

                if (flag) break;
                diff++;
            }
        }

        cout << ret << endl;
    }

    return 0;
}
