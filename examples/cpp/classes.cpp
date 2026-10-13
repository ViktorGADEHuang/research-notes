#include <cmath>
#include <iostream>
#include <stdexcept>

// 把机器人数据与合法操作封装在一起。
class Robot {
public:
    // 构造时直接初始化成员；explicit 避免意外隐式转换。
    // speed_mps 是本次传入的参数，speed_mps_ 是对象一直保存的成员。
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
};

// 程序入口；下面按顺序执行示例步骤。
int main() {
    // 创建一个自己的 Robot 对象，保存速度 0.8 米/秒。
    const Robot robot{0.8};
    std::cout << "distance: " << robot.distance(5.0) << " m\n";
    try {
        const Robot invalid{-1.0};
        // 上面的构造已经抛出异常，本行不会执行。
        std::cout << invalid.distance(1.0) << '\n';
    } catch (const std::invalid_argument& error) {
        // 不让失败继续冒出 main，在这里显示构造失败的原因。
        std::cout << error.what() << '\n';
    }
}
