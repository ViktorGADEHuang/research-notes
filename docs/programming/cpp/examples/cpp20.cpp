#include <concepts>
#include <iostream>
#include <ranges>
#include <span>
#include <stdexcept>
#include <vector>

// concepts 约束 T 为浮点类型，整数调用会被拒绝。
template<std::floating_point T>
T meters_to_centimeters(T meters) {
    return meters * T{100};
}

// 借用连续数据并带长度，不拥有数据，也不延长生命周期。
double mean(std::span<const double> values) {
    if (values.empty()) {
        // 输入不符合函数约定，报告原因而不继续计算。
        throw std::invalid_argument("empty samples");
    }
    double total{0.0};
    for (double value : values) { total += value; }
    return total / static_cast<double>(values.size());
}

// 程序入口；下面按顺序执行示例步骤。
int main() {
    const std::vector<double> distances{1.0, 3.0, 5.0};
    // view 保存处理规则，不立即生成结果列表；不能盲目声明为 const。
    auto far_cm = distances
        // 保留大于 2 米的元素，遍历时筛选。
        | std::views::filter([](double d) { return d > 2.0; })
        // 把筛选后的米转换为厘米，遍历时计算。
        | std::views::transform([](double d) { return meters_to_centimeters(d); });
    // 开始遍历才触发延迟筛选与转换。
    for (double value : far_cm) {
        std::cout << value << ' ';
    }
    std::cout << "\nmean: " << mean(distances) << '\n';
}
