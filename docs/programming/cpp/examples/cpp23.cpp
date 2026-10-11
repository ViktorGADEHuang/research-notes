#include <cmath>
#include <expected>
#include <iostream>
#include <string>
#include <utility>

enum class Mode : unsigned { idle = 0, tracking = 1 };

std::expected<double, std::string> speed(double distance_m, double seconds) {
    if (!std::isfinite(distance_m) || distance_m < 0.0) {
        return std::unexpected(std::string{"invalid distance"});
    }
    if (!std::isfinite(seconds) || seconds <= 0.0) {
        return std::unexpected(std::string{"duration must be positive"});
    }
    const double result = distance_m / seconds;
    if (!std::isfinite(result)) {
        return std::unexpected(std::string{"speed overflow"});
    }
    return result;
}

int main() {
    for (const double seconds : {2.0, 0.0}) {
        const auto result = speed(4.0, seconds);
        if (result) {
            std::cout << "speed: " << *result << " m/s\n";
        } else {
            std::cout << "error: " << result.error() << '\n';
        }
    }
    std::cout << "mode code: " << std::to_underlying(Mode::tracking) << '\n';
}
