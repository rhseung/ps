//
// Created by Hyunseung Ryu on 2025. 8. 8..
//

#include <bits/stdc++.h>
#define endl "\n"

using namespace std;
using ll = long long;

template <class T>
concept Integral = std::is_integral_v<T>;

template <class A, class B>
using CommonAcc = std::common_type_t<A, std::intmax_t>;

template <Integral Q>
constexpr Q norm_mod(Q x, Q mod) noexcept {
    auto r = x % mod;
    return r < 0 ? static_cast<Q>(r + mod) : r;
}

template <typename T>
class Matrix {
private:
    std::size_t n = 0, m = 0; // rows, cols
    std::vector<T> d; // row-major data, size n*m

public:
    // If MOD > 0, all ops on a result Matrix<R> are done modulo Matrix<R>::MOD
    static inline long long MOD = 0; // e.g., Matrix<long long>::MOD = 1'000'000'007;

    // Allow cross-specialization access for mixed-type operators
    template <typename>
    friend class Matrix;

    Matrix() = default;

    Matrix(const std::size_t n_, const std::size_t m_, T val = T{}) : n(n_), m(m_) {
        d.resize(n_ * m_);
        if (MOD) {
            if constexpr (Integral<T>) {
                T mod = static_cast<T>(MOD);
                T norm = norm_mod<T>(val, mod);
                std::fill(d.begin(), d.end(), norm);
            }
            else {
                std::fill(d.begin(), d.end(), val);
            }
        }
        else {
            std::fill(d.begin(), d.end(), val);
        }
    }

    Matrix(std::initializer_list<std::initializer_list<T>> init) {
        n = init.size();
        assert(n > 0);

        m = init.begin()->size();
        for (const auto& row : init)
            assert(row.size() == m);

        d.reserve(n * m);
        for (const auto& row : init) {
            for (const auto& val : row) {
                if (MOD) {
                    if constexpr (Integral<T>) {
                        T mod = static_cast<T>(MOD);
                        d.push_back(norm_mod<T>(val, mod));
                    }
                    else {
                        d.push_back(val);
                    }
                }
                else {
                    d.push_back(val);
                }
            }
        }
    }

    static Matrix identity(std::size_t n_) {
        Matrix I(n_, n_, T{});
        for (std::size_t i = 0; i < n_; ++i) I(i, i) = static_cast<T>(1);
        return I;
    }

    // Element access
    T& operator()(const std::size_t r, const std::size_t c) {
        assert(r < n && c < m);
        return d[r * m + c];
    }

    const T& operator()(const std::size_t r, const std::size_t c) const {
        assert(r < n && c < m);
        return d[r * m + c];
    }

    [[nodiscard]] std::size_t rows() const {
        return n;
    }

    [[nodiscard]] std::size_t cols() const {
        return m;
    }

    bool operator==(const Matrix& o) const noexcept {
        return n == o.n && m == o.m && d == o.d;
    }

    bool operator!=(const Matrix& o) const noexcept {
        return !(*this == o);
    }

    template <typename U>
    bool operator==(const Matrix<U>& o) const noexcept {
        if (n != o.rows() || m != o.cols()) return false;
        using R = std::common_type_t<T, U>;
        for (std::size_t i = 0, N = d.size(); i < N; ++i) {
            if (static_cast<R>(d[i]) != static_cast<R>(o.d[i])) return false;
        }
        return true;
    }

    template <typename U>
    bool operator!=(const Matrix<U>& o) const noexcept {
        return !(*this == o);
    }

    Matrix& operator+=(const Matrix& o) {
        assert(n == o.n && m == o.m);
        if (Matrix<T>::MOD) {
            using Acc = CommonAcc<T, T>;
            const Acc mod = static_cast<Acc>(Matrix<T>::MOD);
            for (std::size_t i = 0; i < d.size(); ++i) {
                Acc a = static_cast<Acc>(d[i]);
                Acc b = static_cast<Acc>(o.d[i]);
                if constexpr (std::is_integral_v<Acc>)
                    d[i] = static_cast<T>(norm_mod<Acc>(a + b, mod));
                else
                    d[i] = static_cast<T>(static_cast<long double>(a + b));
            }
        }
        else {
            for (std::size_t i = 0; i < d.size(); ++i) d[i] += o.d[i];
        }
        return *this;
    }

    template <typename U, typename R = std::common_type_t<T, U>>
    auto operator+(const Matrix<U>& o) const -> Matrix<R> {
        assert(n == o.n && m == o.m);
        Matrix<R> r(n, m, R{});

        if (Matrix<R>::MOD) {
            using Acc = CommonAcc<R, R>;
            const Acc mod = static_cast<Acc>(Matrix<R>::MOD);
            for (std::size_t i = 0; i < d.size(); ++i) {
                Acc a = static_cast<Acc>(static_cast<R>(d[i]));
                Acc b = static_cast<Acc>(static_cast<R>(o.d[i]));
                if constexpr (std::is_integral_v<Acc>)
                    r.d[i] = static_cast<R>(norm_mod<Acc>(a + b, mod));
                else
                    r.d[i] = static_cast<R>(static_cast<long double>(a + b));
            }
        }
        else {
            for (std::size_t i = 0; i < d.size(); ++i)
                r.d[i] = static_cast<R>(d[i]) + static_cast<R>(o.d[i]);
        }
        return r;
    }

    template <typename U, typename R = std::common_type_t<T, U>>
    auto operator*(const Matrix<U>& o) const -> Matrix<R> {
        assert(m == o.n);
        Matrix<R> r(n, o.m, R{});

        if (Matrix<R>::MOD) {
            using Acc = CommonAcc<R, R>;
            const Acc mod = static_cast<Acc>(Matrix<R>::MOD);
            for (std::size_t i = 0; i < n; ++i) {
                for (std::size_t k = 0; k < m; ++k) {
                    Acc aik = static_cast<Acc>(static_cast<R>(d[i * m + k]));
                    if (!aik) continue;
                    for (std::size_t j = 0; j < o.m; ++j) {
                        Acc cur = static_cast<Acc>(static_cast<R>(r.d[i * o.m + j]));
                        Acc b = static_cast<Acc>(static_cast<R>(o.d[k * o.m + j]));
                        Acc sum = cur + aik * b;
                        std::size_t idx = i * o.m + j;
                        if constexpr (std::is_integral_v<Acc>)
                            r.d[idx] = static_cast<R>(norm_mod<Acc>(sum, mod));
                        else
                            r.d[idx] = static_cast<R>(static_cast<long double>(sum));
                    }
                }
            }
        }
        else {
            for (std::size_t i = 0; i < n; ++i) {
                for (std::size_t k = 0; k < m; ++k) {
                    R aik = d[i * m + k];
                    if (!aik) continue;
                    for (std::size_t j = 0; j < o.m; ++j) r.d[i * o.m + j] += aik * static_cast<R>(o.d[k * o.m + j]);
                }
            }
        }
        return r;
    }

    template <typename U, typename R = std::common_type_t<T, U>>
    auto operator*(const std::vector<U>& vec) const -> std::vector<R> {
        assert(m == vec.size());
        std::vector<R> r(n, R{});

        if (Matrix<R>::MOD) {
            using Acc = CommonAcc<R, R>;
            const Acc mod = static_cast<Acc>(Matrix<R>::MOD);
            for (std::size_t i = 0; i < n; ++i) {
                Acc s = 0;
                for (std::size_t k = 0; k < m; ++k) {
                    Acc a = static_cast<Acc>(static_cast<R>(d[i * m + k]));
                    Acc b = static_cast<Acc>(static_cast<R>(vec[k]));
                    s += a * b;
                }
                if constexpr (std::is_integral_v<Acc>)
                    r[i] = static_cast<R>(norm_mod<Acc>(s, mod));
                else
                    r[i] = static_cast<R>(static_cast<long double>(s));
            }
        }
        else {
            for (std::size_t i = 0; i < n; ++i) {
                R s{};
                for (std::size_t k = 0; k < m; ++k) s += static_cast<R>(d[i * m + k]) * static_cast<R>(vec[k]);
                r[i] = s;
            }
        }
        return r;
    }

    template <typename S, typename R = std::common_type_t<T, S>>
    auto operator*(const S& s) const -> Matrix<R> {
        Matrix<R> r(n, m, R{});
        if (Matrix<R>::MOD) {
            using Acc = CommonAcc<R, R>;
            const Acc mod = static_cast<Acc>(Matrix<R>::MOD);
            const Acc b = static_cast<Acc>(static_cast<R>(s));
            for (std::size_t i = 0; i < d.size(); ++i) {
                Acc a = static_cast<Acc>(static_cast<R>(d[i]));
                if constexpr (std::is_integral_v<Acc>)
                    r.d[i] = static_cast<R>(norm_mod<Acc>(a * b, mod));
                else
                    r.d[i] = static_cast<R>(static_cast<long double>(a * b));
            }
        }
        else {
            for (std::size_t i = 0; i < d.size(); ++i) r.d[i] = static_cast<R>(d[i]) * static_cast<R>(s);
        }
        return r;
    }

    template <typename S>
    friend auto operator*(const S& s, const Matrix& A) -> Matrix<std::common_type_t<T, S>> {
        using R = std::common_type_t<T, S>;
        Matrix<R> r(A.n, A.m, R{});
        if (Matrix<R>::MOD) {
            using Acc = CommonAcc<R, R>;
            const Acc mod = static_cast<Acc>(Matrix<R>::MOD);
            const Acc b = static_cast<Acc>(static_cast<R>(s));
            for (std::size_t i = 0; i < A.d.size(); ++i) {
                Acc a = static_cast<Acc>(static_cast<R>(A.d[i]));
                if constexpr (std::is_integral_v<Acc>)
                    r.d[i] = static_cast<R>(norm_mod<Acc>(a * b, mod));
                else
                    r.d[i] = static_cast<R>(static_cast<long double>(a * b));
            }
        }
        else {
            for (std::size_t i = 0; i < A.d.size(); ++i) r.d[i] = static_cast<R>(A.d[i]) * static_cast<R>(s);
        }
        return r;
    }

    template <typename S>
    auto operator*=(const S& s) -> std::enable_if_t<std::is_same_v<std::common_type_t<T, S>, T>, Matrix&> {
        if (Matrix<T>::MOD) {
            using Acc = CommonAcc<T, T>;
            const Acc mod = static_cast<Acc>(Matrix<T>::MOD);
            const Acc b = static_cast<Acc>(static_cast<T>(s));
            for (std::size_t i = 0; i < d.size(); ++i) {
                Acc a = static_cast<Acc>(d[i]);
                if constexpr (std::is_integral_v<Acc>)
                    d[i] = static_cast<T>(norm_mod<Acc>(a * b, mod));
                else
                    d[i] = static_cast<T>(static_cast<long double>(a * b));
            }
        }
        else {
            for (auto& x : d) x = static_cast<T>(x * static_cast<T>(s));
        }
        return *this;
    }

    Matrix pow(long long e) const {
        assert(n == m);
        Matrix base = *this;
        Matrix res = identity(n);
        while (e > 0) {
            if (e & 1LL) res = res * base;
            base = base * base;
            e >>= 1LL;
        }
        return res;
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    ll a, b;
    cin >> a >> b;

    // [Fn+1; Fn] = [1 1; 1 0] * [Fn; Fn-1] = ... = [1 1; 1 0]^n * [F1; F0] = [1 1; 1 0]^n * [1; 0]
    Matrix<ll>::MOD = 1'000'000'000;
    const Matrix<ll> mat = {{1, 1}, {1, 0}};
    const vector<ll> vec = {1, 0}; // F1, F0

    // f_n+1 = f_n + f_n-1 => f_n = -f_n-1 + f_n+1
    // f_1 + f_2 + ... + f_n
    // = (-f_0 + f_2) + (-f_1 + f_3) + (-f_2 + f_4) + ... + (-f_n-3 + f_n-1) + (-f_n-2 + f_n) + (-f_n-1 + f_n+1)
    // = -f_0 - f_1 + f_n + f_n+1
    // = f_n+2 - 1
    // therefore, f_a + f_a+1 + ... + f_b = (f_1 + ... + f_b) - (f_1 + ... + f_a-1) = (f_b+2 - 1) - (f_a+1 - 1) = f_b+2 - f_a+1

    const auto F_A = mat.pow(a) * vec;
    const auto F_B = mat.pow(b + 1) * vec;

    const ll f_b_2 = F_B[0]; // F(b + 2)
    const ll f_a_1 = F_A[0]; // F(a + 1)

    cout << ((f_b_2 - f_a_1 + Matrix<ll>::MOD) % Matrix<ll>::MOD) << endl;

    return 0;
}
