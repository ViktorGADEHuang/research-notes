#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>

// 程序入口；下面按顺序执行示例步骤。
int main() {
    // 四个元素的下标为 0、1、2、3；size() 是元素数量 4。
    std::vector<double> distances{4.0, 1.0, 3.0, 2.0};
    // 对半开区间 [begin, end) 排序，修改原容器。
    std::sort(distances.begin(), distances.end());
    // 统计满足条件的元素，不生成另一个列表。
    const auto close_count = std::count_if(
        distances.begin(), distances.end(),
        // 无捕获 Lambda：每个距离小于等于 2 才算接近。
        [](double d) { return d <= 2.0; });
    // 初值 0.0 让累加保持浮点类型。
    const double sum = std::accumulate(
        distances.begin(), distances.end(), 0.0);
    // 排序后逐项读取；这里只输出数值，不需要修改元素或复制整个容器。
    for (const auto distance : distances) {
        std::cout << distance << ' ';
    }
    std::cout << "\nclose: " << close_count << ", sum: " << sum << '\n';
    // 本例确定非空，at(0) 取第一个元素；若下标越界，at 会抛异常。
    std::cout << "first: " << distances.at(0) << '\n';
}
