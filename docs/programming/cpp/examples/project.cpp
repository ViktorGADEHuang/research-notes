#include <cmath>
#include <iomanip>
#include <iostream>
#include <optional>
#include <span>
#include <unordered_set>
#include <vector>

struct Point { double x_m; double y_m; };
struct Sheep { int id; Point position; };
struct Summary { Point center; int farthest_id; double radius_m; };

std::optional<Summary> summarize(std::span<const Sheep> sheep) {
    if (sheep.empty()) { return std::nullopt; }
    Point center{0.0, 0.0};
    std::unordered_set<int> ids;
    for (const auto& item : sheep) {
        if (!std::isfinite(item.position.x_m)
            || !std::isfinite(item.position.y_m)
            || !ids.insert(item.id).second) {
            return std::nullopt;
        }
        center.x_m += item.position.x_m;
        center.y_m += item.position.y_m;
    }
    const auto count = static_cast<double>(sheep.size());
    center.x_m /= count;
    center.y_m /= count;
    if (!std::isfinite(center.x_m) || !std::isfinite(center.y_m)) {
        return std::nullopt;
    }
    Summary result{center, sheep.front().id, -1.0};
    for (const auto& item : sheep) {
        const double distance = std::hypot(
            item.position.x_m - center.x_m, item.position.y_m - center.y_m);
        if (!std::isfinite(distance)) { return std::nullopt; }
        if (distance > result.radius_m) {
            result.farthest_id = item.id;
            result.radius_m = distance;
        }
    }
    return result;
}

int main() {
    const std::vector<Sheep> frame{{1, {0.0, 0.0}}, {2, {2.0, 0.0}}, {3, {4.0, 3.0}}};
    if (const auto result = summarize(frame)) {
        std::cout << std::fixed << std::setprecision(3);
        std::cout << "center: (" << result->center.x_m << ", "
                  << result->center.y_m << ") m\n";
        std::cout << "farthest id: " << result->farthest_id << '\n';
        std::cout << "radius: " << result->radius_m << " m\n";
    } else {
        std::cout << "invalid frame\n";
    }
    const std::vector<Sheep> empty;
    std::cout << "empty frame accepted: " << std::boolalpha
              << summarize(empty).has_value() << '\n';
}
