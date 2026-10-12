#include <iostream>
#include <numeric>
#include <vector>
#include <stdexcept>

// 只读借用列表，不复制整个容器。
double average(const std::vector<double>& values) {
    // 空列表不能取平均，否则会除以零。
    if (values.empty()) {
        // 输入不符合函数约定，报告原因而不继续计算。
        throw std::invalid_argument("empty samples");
    }
    // 从浮点 0.0 开始累加，避免整数累加造成截断。
    return std::accumulate(values.begin(), values.end(), 0.0)
        / static_cast<double>(values.size());
}

// 可修改引用：这个函数会改变调用者的数据。
void shift(std::vector<double>& values, double offset) {
    // 绑定真实元素；去掉 & 只会修改副本。
    for (auto& value : values) {
        // 给每个元素加同样偏移量。
        value += offset;
    }
}

// 程序入口；下面按顺序执行示例步骤。
int main() {
    std::vector<double> values{1.0, 2.0, 3.0};
    std::cout << "before: " << average(values) << '\n';
    // 调用结束后原列表变为 {2.0, 3.0, 4.0}，所以第二次平均值是 3。
    shift(values, 1.0);
    std::cout << "after: " << average(values) << '\n';
    // try 圈出需要处理失败的操作；异常发生后不会继续执行该路径剩余语句。
    try {
        const std::vector<double> empty;
        std::cout << average(empty) << '\n';
    } catch (const std::invalid_argument& error) {
        // catch 接住前面报告的非法输入，what() 读取说明文字。
        std::cout << error.what() << '\n';
    }
}
