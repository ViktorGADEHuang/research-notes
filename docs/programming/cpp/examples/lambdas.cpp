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
    // 把结果输出到终端，便于与正文中的示例结果对照。
    std::cout << std::boolalpha;
    // 把结果输出到终端，便于与正文中的示例结果对照。
    std::cout << "value capture: " << by_value(3.0) << '\n';
    // 把结果输出到终端，便于与正文中的示例结果对照。
    std::cout << "reference capture: " << by_reference(3.0) << '\n';
    const std::vector<double> distances{1.0, 3.0, 5.0};
    // 把结果输出到终端，便于与正文中的示例结果对照。
    std::cout << "above current threshold: "
              // 算法会调用传入的 Lambda 检查每个元素。
              << std::count_if(distances.begin(), distances.end(), by_reference)
              << '\n';
}
