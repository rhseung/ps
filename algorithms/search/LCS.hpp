//
// Created by Hyunseung Ryu on 2025. 8. 17..
//


#ifndef PS_LCS_HPP
#define PS_LCS_HPP

#include <string>
#include <vector>
#include <algorithm>

namespace search {
    inline size_t length_LCS(const std::string& s1, const std::string& s2) {
        const size_t m = s1.length(), n = s2.length();
        std::vector<std::vector<size_t>> DP(m + 1, std::vector<size_t>(n + 1, 0));

        for (size_t i = 1; i <= m; ++i) {
            for (size_t j = 1; j <= n; ++j) {
                if (s1[i - 1] == s2[j - 1]) {
                    DP[i][j] = DP[i - 1][j - 1] + 1;
                }
                else {
                    DP[i][j] = std::max(DP[i - 1][j], DP[i][j - 1]);
                }
            }
        }

        return DP[m][n];
    }

    inline std::vector<std::vector<size_t>> lengths_LCS(const std::string& s1, const std::string& s2) {
        const size_t m = s1.length(), n = s2.length();
        std::vector<std::vector<size_t>> DP(m + 1, std::vector<size_t>(n + 1, 0));

        for (size_t i = 1; i <= m; ++i) {
            for (size_t j = 1; j <= n; ++j) {
                if (s1[i - 1] == s2[j - 1]) {
                    DP[i][j] = DP[i - 1][j - 1] + 1;
                }
                else {
                    DP[i][j] = std::max(DP[i][j - 1], DP[i - 1][j]);
                }
            }
        }

        return DP;
    }

    inline std::string backtrack_LCS(
        const std::vector<std::vector<size_t>>& DP,
        const std::string& s1,
        const std::string& s2,
        const size_t i,
        const size_t j
    ) {
        if (i == 0 || j == 0)
            return "";
        else if (s1[i - 1] == s2[j - 1])
            return backtrack_LCS(DP, s1, s2, i - 1, j - 1) + s1[i - 1];
        else if (DP[i - 1][j] >= DP[i][j - 1])
            return backtrack_LCS(DP, s1, s2, i - 1, j);
        else
            return backtrack_LCS(DP, s1, s2, i, j - 1);
    }

    inline std::string find_LCS(
        const std::string& s1,
        const std::string& s2
    ) {
        const auto DP = lengths_LCS(s1, s2);
        return backtrack_LCS(DP, s1, s2, s1.length(), s2.length());
    }
}

#endif //PS_LCS_HPP
