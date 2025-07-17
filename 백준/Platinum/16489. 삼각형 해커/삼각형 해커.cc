#include <bits/stdc++.h>
#define endl "\n"
#define INF 0x3f3f3f3f

using namespace std;
typedef long long int lnt;

double surface_sq(const double a, const double b, const double c) {
  const double s = (a + b + c) / 2;
  return s * (s - a) * (s - b) * (s - c);
}

double inner_radius_sq(const double S_sq, const double a, const double b,
                       const double c) {
  const double outline = a + b + c;
  return 4 * S_sq / (outline * outline);
}

double outer_radius_sq(const double S_sq, const double a, const double b,
                       const double c) {
  const double product = a * b * c;
  return product * product / (16 * S_sq);
}

double distance_sq(const double R_sq, const double r_sq) {
  return R_sq - 2 * sqrt(R_sq * r_sq);
}

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);
  cout.tie(nullptr);

  double a, b, c;
  cin >> a >> b >> c;

  const double S_sq = surface_sq(a, b, c);
  const double R_sq = outer_radius_sq(S_sq, a, b, c);
  const double r_sq = inner_radius_sq(S_sq, a, b, c);
  const double d_sq = distance_sq(R_sq, r_sq);

  const double h1 = sqrt(R_sq - (a / 2) * (a / 2));
  const double h2 = sqrt(R_sq - (b / 2) * (b / 2));
  const double h3 = sqrt(R_sq - (c / 2) * (c / 2));
  double k = h1 + h2 + h3;

  printf("%.12lf\n%.12lf\n%.12lf\n%.12lf\n%.12lf\n", sqrt(S_sq), sqrt(R_sq),
         sqrt(r_sq), sqrt(d_sq), k);

  return 0;
}