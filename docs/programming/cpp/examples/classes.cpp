#include <cmath>
#include <iostream>
#include <stdexcept>
#include <vector>

class Robot {
public:
    explicit Robot(double speed_mps) : speed_mps_{speed_mps} {
        if (!std::isfinite(speed_mps) || speed_mps < 0.0) {
            throw std::invalid_argument("invalid speed");
        }
    }
    double distance(double seconds) const {
        if (!std::isfinite(seconds) || seconds < 0.0) {
            throw std::invalid_argument("invalid duration");
        }
        return speed_mps_ * seconds;
    }
private:
    double speed_mps_;
    std::vector<double> observations_; // Automatically releases its memory.
};

int main() {
    const Robot robot{0.8};
    std::cout << "distance: " << robot.distance(5.0) << " m\n";
    try {
        const Robot invalid{-1.0};
        std::cout << invalid.distance(1.0) << '\n';
    } catch (const std::invalid_argument& error) {
        std::cout << error.what() << '\n';
    }
}
