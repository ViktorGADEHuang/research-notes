#include <concepts>
#include <iostream>
#include <ranges>
#include <span>
#include <stdexcept>
#include <vector>

template<std::floating_point T>
T meters_to_centimeters(T meters) {
    return meters * T{100};
}

double mean(std::span<const double> values) {
    if (values.empty()) {
        throw std::invalid_argument("empty samples");
    }
    double total{0.0};
    for (double value : values) { total += value; }
    return total / static_cast<double>(values.size());
}

int main() {
    const std::vector<double> distances{1.0, 3.0, 5.0};
    auto far_cm = distances
        | std::views::filter([](double d) { return d > 2.0; })
        | std::views::transform([](double d) { return meters_to_centimeters(d); });
    for (double value : far_cm) {
        std::cout << value << ' ';
    }
    std::cout << "\nmean: " << mean(distances) << '\n';
}
