#include <iostream>
#include <string>
#include <vector>

int main() {
    const std::string experiment{"herding-demo"};
    const double threshold_m{3.0};
    const std::vector<double> distances_m{1.2, 4.5, 2.0};
    int far_count{0};
    for (const double distance_m : distances_m) {
        if (distance_m > threshold_m) {
            ++far_count;
        }
    }
    std::cout << experiment << '\n';
    std::cout << "far sheep: " << far_count << '\n';
    std::cout << "integer: " << 5 / 2 << ", decimal: " << 5.0 / 2 << '\n';
}
