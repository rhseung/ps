// BOJ 15576 - 큰 수 곱셈 (2)
#include <bits/stdc++.h>
#include <ranges>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

#include <complex>
#include <numbers>
#define all(x) (x).begin(), (x).end()
#define sz(x)  int((x).size())

using base = std::complex<double>;

constexpr double PI = std::numbers::pi;
constexpr int mod = 998244353;

namespace math {
    using real_t = double;
    using base = complex<real_t>;

    inline void fft(vector<base>& a, const bool inv) {
        int n = a.size(), j = 0;
        vector<base> roots(n / 2);

        for (int i = 1; i < n; i++) {
            int bit = (n >> 1);
            while (j >= bit) {
                j -= bit;
                bit >>= 1;
            }
            j += bit;
            if (i < j) swap(a[i], a[j]);
        }

        const real_t ang = 2 * acos(static_cast<real_t>(-1)) / n * (inv ? -1 : 1);
        for (int i = 0; i < n / 2; i++) {
            roots[i] = base(cos(ang * i), sin(ang * i));
        }

        /*
        XOR Convolution : set roots[*] = 1.
        OR Convolution : set roots[*] = 1, and do following:
        if (!inv) {
        a[j + k] = u + v;
        a[j + k + i/2] = u;
        } else {
        a[j + k] = v;
        a[j + k + i/2] = u - v;
        }
        */
        for (int i = 2; i <= n; i <<= 1) {
            int step = n / i;
            for (int j = 0; j < n; j += i) {
                for (int k = 0; k < i / 2; k++) {
                    base u = a[j + k], v = a[j + k + i / 2] * roots[step * k];
                    a[j + k] = u + v;
                    a[j + k + i / 2] = u - v;
                }
            }
        }
        if (inv) for (int i = 0; i < n; i++) a[i] /= n; // skip for OR convolution.
    }

    template <typename T>
    void ntt(vector<T>& a, const bool inv) {
        const int prr = 3; // primitive root
        int n = a.size(), j = 0;
        vector<T> roots(n / 2);
        for (int i = 1; i < n; i++) {
            int bit = (n >> 1);
            while (j >= bit) {
                j -= bit;
                bit >>= 1;
            }
            j += bit;
            if (i < j) swap(a[i], a[j]);
        }

        T ang = ipow(T(prr), (mod - 1) / n);
        if (inv) ang = T(1) / ang;
        for (int i = 0; i < n / 2; i++) {
            roots[i] = (i ? (roots[i - 1] * ang) : T(1));
        }

        for (int i = 2; i <= n; i <<= 1) {
            int step = n / i;
            for (int j = 0; j < n; j += i) {
                for (int k = 0; k < i / 2; k++) {
                    T u = a[j + k], v = a[j + k + i / 2] * roots[step * k];
                    a[j + k] = u + v;
                    a[j + k + i / 2] = u - v;
                }
            }
        }
        if (inv) {
            T rev = T(1) / T(n);
            for (int i = 0; i < n; i++) a[i] *= rev;
        }
    }

    template <typename T>
    vector<T> multiply_ntt(vector<T>& v, const vector<T>& w) {
        vector<T> fv(all(v)), fw(all(w));
        int n = 2;
        while (n < sz(v) + sz(w)) n <<= 1;
        fv.resize(n);
        fw.resize(n);
        ntt(fv, false);
        ntt(fw, false);
        for (int i = 0; i < n; i++) fv[i] *= fw[i];
        ntt(fv, true);
        vector<T> ret(n);
        for (int i = 0; i < n; i++) ret[i] = fv[i];
        return ret;
    }

    /**
     * FFT based polynomial multiplication. O(NlogN)
     * @note 받아 올림 처리는 따로 해줘야 함. 각 배열의 원소가 받아 올림에 의해 10을 넘을 수 있음
     * @tparam T
     * @param v
     * @param w
     * @return
     */
    template <typename T>
    vector<T> multiply(vector<T>& v, const vector<T>& w) {
        vector<base> fv(all(v)), fw(all(w));
        int n = 2;
        while (n < sz(v) + sz(w)) n <<= 1;
        fv.resize(n);
        fw.resize(n);
        fft(fv, false);
        fft(fw, false);
        for (int i = 0; i < n; i++) fv[i] *= fw[i];
        fft(fv, true);
        vector<T> ret(n);
        for (int i = 0; i < n; i++) ret[i] = static_cast<T>(llround(fv[i].real()));
        return ret;
    }

    template <typename T>
    vector<T> multiply_mod(vector<T> v, const vector<T>& w) {
        int n = 2;
        while (n < sz(v) + sz(w)) n <<= 1;
        vector<base> v1(n), v2(n), r1(n), r2(n);
        for (int i = 0; i < v.size(); i++) {
            v1[i] = base(v[i] >> 15, v[i] & 32767);
        }
        for (int i = 0; i < w.size(); i++) {
            v2[i] = base(w[i] >> 15, w[i] & 32767);
        }
        fft(v1, false);
        fft(v2, false);
        for (int i = 0; i < n; i++) {
            int j = (i ? (n - i) : i);
            base ans1 = (v1[i] + conj(v1[j])) * base(0.5, 0);
            base ans2 = (v1[i] - conj(v1[j])) * base(0, -0.5);
            base ans3 = (v2[i] + conj(v2[j])) * base(0.5, 0);
            base ans4 = (v2[i] - conj(v2[j])) * base(0, -0.5);
            r1[i] = (ans1 * ans3) + (ans1 * ans4) * base(0, 1);
            r2[i] = (ans2 * ans3) + (ans2 * ans4) * base(0, 1);
        }
        fft(r1, true);
        fft(r2, true);
        vector<T> ret(n);
        for (int i = 0; i < n; i++) {
            T av = llround(r1[i].real());
            T bv = llround(r1[i].imag()) + llround(r2[i].real());
            T cv = llround(r2[i].imag());
            av = av << 30;
            bv = bv << 15;
            ret[i] = av + bv + cv;
        }
        return ret;
    }

    template <typename T>
    vector<T> multiply_naive(vector<T> v, const vector<T>& w) {
        if (sz(v) == 0 || sz(w) == 0) return vector<T>();
        vector<T> ret(sz(v) + sz(w) - 1);
        for (int i = 0; i < sz(v); i++) {
            for (int j = 0; j < sz(w); j++) {
                ret[i + j] += v[i] * w[j];
            }
        }
        return ret;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    string a, b;
    cin >> a >> b;

    ranges::reverse(a);
    ranges::reverse(b);

    vector<int> A, B;
    for (const char c : a) A.push_back(c - '0');
    for (const char c : b) B.push_back(c - '0');

    auto C = math::multiply(A, B);
    C.resize(A.size() + B.size() - 1);

    int carry = 0;
    for (int& x : C) {
        const int cur = x + carry;
        x = cur % 10;
        carry = cur / 10;
    }
    while (carry > 0) {
        C.push_back(carry % 10);
        carry /= 10;
    }

    while (C.size() > 1 && C.back() == 0) C.pop_back();

    for (const int& it : std::ranges::reverse_view(C)) {
        cout << it;
    }

    return 0;
}
