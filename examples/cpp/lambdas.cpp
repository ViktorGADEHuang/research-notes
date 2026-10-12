#include <algorithm>
#include <iostream>
#include <vector>

// 程序入口；下面按顺序执行示例步骤。
int main() {
    double threshold{2.0};
    // 保存此刻阈值的副本，之后外部修改不会同步进去。
    const auto by_value = [threshold](double d) { return d > threshold; };
    // 借用外部阈值，使用时必须确保原变量还活着。
    const auto by_reference = [&threshold](double d) { return d > threshold; };
    // 修改原变量，用来展示两种捕获方式的差别。
    threshold = 4.0;
    // boolalpha 让判断结果显示为 true / false，便于对照纸上推演。
    std::cout << std::boolalpha;
    std::cout << "value capture: " << by_value(3.0) << '\n';
    std::cout << "reference capture: " << by_reference(3.0) << '\n';
    const std::vector<double> distances{1.0, 3.0, 5.0};
    // count_if 遍历距离，每次调用 by_reference(当前距离)。
    // 只有 5.0 大于现在的 4.0，所以最终计数是 1。
    std::cout << "above current threshold: "
              << std::count_if(distances.begin(), distances.end(), by_reference)
              << '\n';
}
