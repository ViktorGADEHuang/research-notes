#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    double threshold{2.0};
    const auto by_value = [threshold](double d) { return d > threshold; };
    const auto by_reference = [&threshold](double d) { return d > threshold; };
    threshold = 4.0;
    std::cout << std::boolalpha;
    std::cout << "value capture: " << by_value(3.0) << '\n';
    std::cout << "reference capture: " << by_reference(3.0) << '\n';
    const std::vector<double> distances{1.0, 3.0, 5.0};
    std::cout << "above current threshold: "
              << std::count_if(distances.begin(), distances.end(), by_reference)
              << '\n';
}
