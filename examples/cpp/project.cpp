#include <cmath>
#include <iomanip>
#include <iostream>
#include <optional>
#include <span>
#include <unordered_set>
#include <vector>

// 同一个二维坐标系中的位置，单位米。
struct Point { double x_m; double y_m; };
struct Sheep { int id; Point position; };
// 统计结果：中心、最远个体编号、到中心的距离。
struct Summary { Point center; int farthest_id; double radius_m; };

// 只读借用一帧，无法统计时返回没有值。
std::optional<Summary> summarize(std::span<const Sheep> sheep) {
    // 返回“没有结果”，不要把缺失数据当作有效的零值。
    if (sheep.empty()) { return std::nullopt; }
    Point center{0.0, 0.0};
    // 用集合检查编号唯一，不依赖数据先排序。
    std::unordered_set<int> ids;
    for (const auto& item : sheep) {
        if (!std::isfinite(item.position.x_m)
            || !std::isfinite(item.position.y_m)
            // insert 的 second 表示是否新插入；重复编号会得到 false。
            || !ids.insert(item.id).second) {
            // 返回“没有结果”，不要把缺失数据当作有效的零值。
            return std::nullopt;
        }
        // 累加所有 x 坐标，之后除以数量得到平均值。
        center.x_m += item.position.x_m;
        // y 坐标用同样的方法累加。
        center.y_m += item.position.y_m;
    }
    const auto count = static_cast<double>(sheep.size());
    center.x_m /= count;
    center.y_m /= count;
    if (!std::isfinite(center.x_m) || !std::isfinite(center.y_m)) {
        // 返回“没有结果”，不要把缺失数据当作有效的零值。
        return std::nullopt;
    }
    // 半径从 -1 开始，即使全部重合也能选出第一个编号。
    Summary result{center, sheep.front().id, -1.0};
    for (const auto& item : sheep) {
        // 用二维坐标差计算欧氏距离。
        const double distance = std::hypot(
            item.position.x_m - center.x_m, item.position.y_m - center.y_m);
        // 返回“没有结果”，不要把缺失数据当作有效的零值。
        if (!std::isfinite(distance)) { return std::nullopt; }
        // 发现更远个体才替换；平局保留输入中先出现的个体。
        if (distance > result.radius_m) {
            result.farthest_id = item.id;
            result.radius_m = distance;
        }
    }
    return result;
}

// 程序入口；下面按顺序执行示例步骤。
int main() {
    // 示例帧，不是实时采集或机器人控制输入。
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
