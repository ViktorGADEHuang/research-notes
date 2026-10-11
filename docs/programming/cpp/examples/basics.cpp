#include <iostream>
#include <string>
#include <vector>

// 程序入口；下面按顺序执行示例步骤。
int main() {
    // 实验名初始化后不修改。
    const std::string experiment{"herding-demo"};
    // 距离阈值，单位米；用名字说明物理含义。
    const double threshold_m{3.0};
    // 列表拥有三个距离元素，数量由容器管理。
    const std::vector<double> distances_m{1.2, 4.5, 2.0};
    int far_count{0};
    // 范围循环，每次读取一个距离。
    for (const double distance_m : distances_m) {
        // 严格大于阈值才计数，等于阈值不计入。
        if (distance_m > threshold_m) {
            // 当前这一只满足条件，计数加一。
            ++far_count;
        }
    }
    std::cout << experiment << '\n';
    std::cout << "far sheep: " << far_count << '\n';
    std::cout << "integer: " << 5 / 2 << ", decimal: " << 5.0 / 2 << '\n';
}
