#include <iostream>
#include <numeric>
#include <vector>
#include <stdexcept>

double average(const std::vector<double>& values) {
    if (values.empty()) {
        throw std::invalid_argument("empty samples");
    }
    return std::accumulate(values.begin(), values.end(), 0.0)
        / static_cast<double>(values.size());
}

void shift(std::vector<double>& values, double offset) {
    for (auto& value : values) {
        value += offset;
    }
}

int main() {
    std::vector<double> values{1.0, 2.0, 3.0};
    std::cout << "before: " << average(values) << '\n';
    shift(values, 1.0);
    std::cout << "after: " << average(values) << '\n';
    try {
        const std::vector<double> empty;
        std::cout << average(empty) << '\n';
    } catch (const std::invalid_argument& error) {
        std::cout << error.what() << '\n';
    }
}
