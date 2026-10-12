#include <cmath>
#include <expected>
#include <iostream>
#include <string>
#include <utility>

// 给工作状态起名字；它是状态标签，不参与速度计算。
enum class Mode : unsigned { idle = 0, tracking = 1 };

// 成功时装速度，失败时装字符串原因。
std::expected<double, std::string> speed(double distance_m, double seconds) {
    // 距离允许为 0，但不允许负数、NaN 或无穷大。
    if (!std::isfinite(distance_m) || distance_m < 0.0) {
        // expected 的失败分支：明确返回错误原因。
        return std::unexpected(std::string{"invalid distance"});
    }
    // 时长必须严格大于 0，通过本关之后才执行除法。
    if (!std::isfinite(seconds) || seconds <= 0.0) {
        // expected 的失败分支：明确返回错误原因。
        return std::unexpected(std::string{"duration must be positive"});
    }
    const double result = distance_m / seconds;
    // 两个输入有限，也不能保证相除后的结果一定在 double 可表示范围内。
    if (!std::isfinite(result)) {
        // expected 的失败分支：明确返回错误原因。
        return std::unexpected(std::string{"speed overflow"});
    }
    // 返回普通 double，由 expected 包装为“成功并持有速度”。
    return result;
}

// 程序入口；下面按顺序执行示例步骤。
int main() {
    for (const double seconds : {2.0, 0.0}) {
        const auto result = speed(4.0, seconds);
        // 先确认成功，成功时才能使用 *result。
        if (result) {
            std::cout << "speed: " << *result << " m/s\n";
        } else {
            // 只在失败分支读取错误原因。
            std::cout << "error: " << result.error() << '\n';
        }
    }
    // 显式取枚举的底层值，避免不受控制的隐式转换。
    std::cout << "mode code: " << std::to_underlying(Mode::tracking) << '\n';
}
