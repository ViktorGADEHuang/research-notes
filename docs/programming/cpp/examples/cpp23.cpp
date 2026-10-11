#include <cmath>
#include <expected>
#include <iostream>
#include <string>
#include <utility>

enum class Mode : unsigned { idle = 0, tracking = 1 };

// 成功时装速度，失败时装字符串原因。
std::expected<double, std::string> speed(double distance_m, double seconds) {
    // 检查数值有限及输入范围，避免非法时长或距离。
    if (!std::isfinite(distance_m) || distance_m < 0.0) {
        // expected 的失败分支：明确返回错误原因。
        return std::unexpected(std::string{"invalid distance"});
    }
    // 检查数值有限及输入范围，避免非法时长或距离。
    if (!std::isfinite(seconds) || seconds <= 0.0) {
        // expected 的失败分支：明确返回错误原因。
        return std::unexpected(std::string{"duration must be positive"});
    }
    const double result = distance_m / seconds;
    // 检查数值有限及输入范围，避免非法时长或距离。
    if (!std::isfinite(result)) {
        // expected 的失败分支：明确返回错误原因。
        return std::unexpected(std::string{"speed overflow"});
    }
    return result;
}

// 程序入口；下面按顺序执行示例步骤。
int main() {
    for (const double seconds : {2.0, 0.0}) {
        const auto result = speed(4.0, seconds);
        // 先确认成功，成功时才能使用 *result。
        if (result) {
            // 把结果输出到终端，便于与正文中的示例结果对照。
            std::cout << "speed: " << *result << " m/s\n";
        } else {
            // 只在失败分支读取错误原因。
            std::cout << "error: " << result.error() << '\n';
        }
    }
    // 显式取枚举的底层值，避免不受控制的隐式转换。
    std::cout << "mode code: " << std::to_underlying(Mode::tracking) << '\n';
}
