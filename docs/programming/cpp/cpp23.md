# 12 · C++23：用 expected 表达失败

**示例标准：C++23** · [下载完整代码](examples/cpp23.cpp)

“计算成功得到速度”与“计算失败得到原因”是两种结果。`std::expected<T, E>` 把它们放进同一个返回类型：成功装 T，失败装 E。

## optional、expected 和异常怎么选

| 方式 | 适合什么 | 调用者如何处理 |
| --- | --- | --- |
| `optional<T>` | 没有值就够了，不需要原因 | 检查有没有值 |
| `expected<T, E>` | 失败是正常可能性，需要解释 | 检查成功，读值或错误 |
| 异常 | 不能正常完成操作，需要跨调用层报告 | 匹配的 catch 处理 |

这是接口选择，不是某一种永远最好。`expected` 不阻止被调用代码抛异常，也不会替你检查所有输入。

本章的 `expected` 和 `std::to_underlying` 属于 C++23。编译器接受 `-std=c++23` 不代表配套标准库实现了每个功能；若找不到 `<expected>`，检查编译器和标准库版本。

## 完整示例

```cpp
#include <cmath>
#include <expected>
#include <iostream>
#include <string>
#include <utility>

enum class Mode : unsigned { idle = 0, tracking = 1 };

std::expected<double, std::string> speed(double distance_m, double seconds) {
    if (!std::isfinite(distance_m) || distance_m < 0.0) {
        return std::unexpected(std::string{"invalid distance"});
    }
    if (!std::isfinite(seconds) || seconds <= 0.0) {
        return std::unexpected(std::string{"duration must be positive"});
    }
    const double result = distance_m / seconds;
    if (!std::isfinite(result)) {
        return std::unexpected(std::string{"speed overflow"});
    }
    return result;
}

int main() {
    for (const double seconds : {2.0, 0.0}) {
        const auto result = speed(4.0, seconds);
        if (result) {
            std::cout << "speed: " << *result << " m/s\n";
        } else {
            std::cout << "error: " << result.error() << '\n';
        }
    }
    std::cout << "mode code: " << std::to_underlying(Mode::tracking) << '\n';
}
```

## 编译与运行

在示例目录执行。Windows 使用 PowerShell；Linux/macOS 将 `./cpp23.exe` 换成 `./cpp23`，并把输出文件名的 `.exe` 去掉。

```powershell
g++ -std=c++23 -Wall -Wextra -Wpedantic cpp23.cpp -o cpp23.exe
./cpp23.exe
```

预期输出：

```text
speed: 2 m/s
error: duration must be positive
mode code: 1
```

## 怎样读这段代码

返回普通 `double` 就代表成功；`std::unexpected` 标记这是错误分支。`if (result)` 检查是否成功，成功时 `*result` 读值，失败时 `error()` 读原因。只有失败时才能调用 `error()`。

代码拒绝负距离、非有限数、非正时长，并检查除法结果是否有限。它只是演示计算接口，还没有验证传感器来源、坐标系和物理可行速度。

`enum class` 防止枚举值随意当整数用，`to_underlying` 明确取出底层数值，适合协议编码边界。C++23 还提供 `std::print`、ranges 新工具等；本教程先用传统输出保持示例依赖少，不要求一次学完新特性。

## 常见错误

- 在失败的 expected 上直接 `*result` 不安全；`value()` 会在无值时抛异常。
- `expected<double, string>` 不是同时拥有一个有效速度和一个错误原因；它表示其中一种状态。
- 即便数值有效，也必须另行验证单位和业务限制。

## 动手练习

给 speed 增加最大速度 2 m/s 的要求，超过时返回 speed limit exceeded。

??? tip "展开参考答案"

    在返回成功前检查 `if (result > 2.0) return std::unexpected(std::string{"speed limit exceeded"});`。测试 `speed(4.0, 1.0)` 应失败；`speed(4.0, 2.0)` 应成功。

## 延伸阅读

[规范或官方指南](https://eel.is/c++draft/expected)。标准草案会继续更新，查阅时注意条款可能包含晚于本章示例的功能。


---

[返回学习路线](index.md) · [上一章：11 · C++20：概念、范围与 span](cpp20.md) · [下一章：13 · 并发与线程 →](concurrency.md)
