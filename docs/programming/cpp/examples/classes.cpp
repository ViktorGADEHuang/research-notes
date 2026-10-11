#include <cmath>
#include <iostream>
#include <stdexcept>
#include <vector>

// 把机器人数据与合法操作封装在一起。
class Robot {
public:
    // 构造时直接初始化成员；explicit 避免意外隐式转换。
    explicit Robot(double speed_mps) : speed_mps_{speed_mps} {
        // 拒绝 NaN/无穷大，也检查物理量不为负。
        if (!std::isfinite(speed_mps) || speed_mps < 0.0) {
            // 输入不符合函数约定，报告原因而不继续计算。
            throw std::invalid_argument("invalid speed");
        }
    }
    // 末尾 const 表示这个操作不修改普通成员。
    double distance(double seconds) const {
        // 拒绝 NaN/无穷大，也检查物理量不为负。
        if (!std::isfinite(seconds) || seconds < 0.0) {
            // 输入不符合函数约定，报告原因而不继续计算。
            throw std::invalid_argument("invalid duration");
        }
        // 米/秒乘秒得到米。
        return speed_mps_ * seconds;
    }
// 外部代码不能绕过接口随意修改速度。
private:
    double speed_mps_;
    // 容器自动管理内存，不需要自定义 delete 或析构。
    std::vector<double> observations_; // Automatically releases its memory.
};

// 程序入口；下面按顺序执行示例步骤。
int main() {
    const Robot robot{0.8};
    std::cout << "distance: " << robot.distance(5.0) << " m\n";
    try {
        const Robot invalid{-1.0};
        std::cout << invalid.distance(1.0) << '\n';
    // 处理对应类型的异常；通过 const 引用避免复制异常对象。
    } catch (const std::invalid_argument& error) {
        std::cout << error.what() << '\n';
    }
}
