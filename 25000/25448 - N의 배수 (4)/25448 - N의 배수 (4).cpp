// BOJ 25448 - N의 배수 (4)
#include <iostream>
#include <numeric>
#include <vector>
#define endl "\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

inline ll mod(ll a, ll b) {
    ll r = a % b;
    if (r != 0 && r < 0 != b < 0) {
        r += b;
    }

    return r;
}

inline ll modpow(ll a, ll b, const ll c) {
    ll ret = 1;
    while (b) {
        if (b & 1) ret = ret * a % c;
        b >>= 1;
        a = a * a % c;
    }
    return ret;
}

inline ll modinv(ll d, ll p) {
    return modpow(d, p - 2, p);
}

inline ll find(ll p, vector<bool>& T_c, ll d, ll u, ll v) {
    ll d_inv = modinv(d, p);
    ll left = mod(u * d_inv, p);
    ll right = p + mod(v * d_inv, p);

    while (left < right) {
        ll m = (left + right) / 2;
        ll i = mod(mod(m, p) * d, p);

        if (T_c[i])
            left = m + 1;
        else
            right = m;
    }

    return mod(mod(right, p) * d, p);
}

inline vector<bool> prime_egz(ll p, vector<ll>& N) {
    vector<ll> K(2 * p - 1);
    iota(K.begin(), K.end(), 0);

    sort(K.begin(), K.end(), [&](const ll a, const ll b) {
        return mod(N[a], p) < mod(N[b], p);
    });

    vector<bool> R(2 * p - 1, false);
    for (ll i = 0; i < p - 1; ++i) {
        if (mod(N[K[1 + i]], p) == mod(N[K[p + i]], p)) {
            for (ll j = i + 1; j < i + p + 1; ++j)
                R[K[j]] = true;
            return R;
        }
    }

    ll s = 0;
    for (ll i = 0; i < p; ++i)
        s = mod(s + N[K[i]], p);

    vector<bool> T_c(p, false);
    vector<ll> T_indices(p);

    T_c[s] = true;
    for (ll i = 1; i < p; ++i) {
        if (T_c[0]) break;

        ll diff = mod(N[K[p + i - 1]] - N[K[i]], p);
        ll t = find(p, T_c, diff, s, 0);
        T_c[t] = true;
        T_indices[t] = i;
    }

    for (ll i = 0; i < p; ++i) {
        R[K[i]] = true;
    }

    ll c = 0;
    while (s != c) {
        ll idx = T_indices[c];
        R[K[p + idx - 1]] = true;
        R[K[idx]] = false;
        ll diff = mod(N[K[p + idx - 1]] - N[K[idx]], p);
        c = mod(c - diff + p, p);
    }

    return R;
}

vector<bool> egz(ll n, vector<ll>& N);

inline vector<bool> composite_egz(ll p, ll q, vector<ll>& N) {
    vector<ll> S(p - 1);
    iota(S.begin(), S.end(), 0);

    vector<vector<ll>> T_group(2 * q - 1);

    for (ll i = 0; i < 2 * q - 1; ++i) {
        ll start = (i + 1) * p - 1;
        ll end = (i + 2) * p - 1;
        for (ll val = start; val < end; ++val)
            S.push_back(val);

        vector<ll> N_sub(S.size());
        for (ll j = 0; j < S.size(); ++j)
            N_sub[j] = N[S[j]];

        vector<bool> R_p = egz(p, N_sub);

        vector<ll> selected, not_selected;
        for (ll j = 0; j < 2 * p - 1; ++j) {
            if (R_p[j])
                selected.push_back(S[j]);
            else
                not_selected.push_back(S[j]);
        }

        T_group[i] = selected;
        S = not_selected;
    }

    vector<bool> R(2 * p * q - 1, false);
    vector<ll> S_div_p;

    for (ll i = 0; i < 2 * q - 1; ++i) {
        auto group = T_group[i];
        ll total = 0;
        for (auto idx: group)
            total += N[idx];
        S_div_p.push_back(total / p);
    }

    vector<bool> R_q = egz(q, S_div_p);

    for (ll i = 0; i < 2 * q - 1; ++i) {
        if (R_q[i]) {
            auto group = T_group[i];
            for (auto idx: group)
                R[idx] = true;
        }
    }

    return R;
}

vector<bool> egz(ll n, vector<ll>& N) {
    if (n == 1)
        return {true};

    for (ll i = 2; i < n; ++i) {
        if (n % i == 0)
            return composite_egz(i, n / i, N);
    }

    return prime_egz(n, N);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    ll n;
    cin >> n;

    vector<ll> N(2 * n - 1);
    for (ll i = 0; i < 2 * n - 1; ++i)
        cin >> N[i];

    auto R = egz(n, N);
    for (ll i = 0; i < 2 * n - 1; ++i) {
        if (R[i])
            cout << N[i] << " ";
    }

    return 0;
}
