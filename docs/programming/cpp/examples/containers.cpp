#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>

int main() {
    std::vector<double> distances{4.0, 1.0, 3.0, 2.0};
    std::sort(distances.begin(), distances.end());
    const auto close_count = std::count_if(
        distances.begin(), distances.end(),
        [](double d) { return d <= 2.0; });
    const double sum = std::accumulate(
        distances.begin(), distances.end(), 0.0);
    for (const auto distance : distances) {
        std::cout << distance << ' ';
    }
    std::cout << "\nclose: " << close_count << ", sum: " << sum << '\n';
    std::cout << "first: " << distances.at(0) << '\n';
}
