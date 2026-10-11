# 12 · C++23：用 expected 表达失败

**示例标准：C++23**

“计算成功得到速度”与“计算失败得到原因”是两种结果。`std::expected<T, E>` 把它们放进同一个返回类型：成功装 T，失败装 E。


!!! tip "读完这页，你应该能做到"

    只在成功分支取值，只在失败分支读取错误原因。

    **先会这些就够了**：optional、判断分支。


## 看图梳理

![expected 的两条结果路径](../../assets/learning/cpp-cpp23.svg){ .learning-figure }

[打开大图](../../assets/learning/cpp-cpp23.svg)

**检查输入**：单位与有限数，时长必须大于 0；**成功分支**：expected 保存速度，确认成功后取值；**失败分支**：unexpected 保存原因，error 只在失败时读取。


## 把成功和失败都当成接口的正常输出

算速度时，4 米除以 2 秒可以得到 2 米/秒；除以 0 秒不符合输入约定。调用者需要知道失败原因，不能把 0 速度或 −1 速度当成万能错误标记。

`std::expected<double, std::string>` 可以先读成：“成功得到一个小数，失败得到一段说明”。它在某一时刻处于其中一个状态。`std::unexpected(...)` 用来标记返回的是失败说明，而不是正常结果。

| 函数里 | 调用者里 |
| --- | --- |
| 输入合法，返回 result | if 成立，读取 *result |
| 时长为 0，返回 unexpected | else 分支，读取 error() |

先检查状态，再读对应内容。`if (result)` 判断成功与否，不是判断速度是否大于 0；有效速度为 0 也仍然成功。expected 只是表达结果的方式，是否需要限制最大速度等业务条件，要由你定义并检查。


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
            std::cout << "speed: " << *result << " m/s\n";
        } else {
            // 只在失败分支读取错误原因。
            std::cout << "error: " << result.error() << '\n';
        }
    }
    // 显式取枚举的底层值，避免不受控制的隐式转换。
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

<div class="practice-card" markdown="1">

<p class="practice-kicker">接着正文做一个小改动</p>

<p class="practice-title">计算成功，还要检查业务限制</p>

原 speed 函数检查数值是否合法。现在再加入最大速度要求，区分“除法能算”与“结果符合约定”。

**从哪里开始**：在 cpp23.cpp 的 speed 函数中，result 的非有限检查之后、return result; 之前插入限制检查。

**按这几步做**：

1. 约定最大速度为 2 m/s，恰好 2 仍允许。
2. 大于上限时返回 unexpected，保留已有输入检查。
3. 比较 speed(4.0, 1.0) 与 speed(4.0, 2.0)。

??? tip "需要一点提示？"

    速度是距离除以时长：4 / 1 = 4，4 / 2 = 2。不要把条件写成 >= 2。

??? example "查看参考修改与解释"

    前者因 4 m/s 超过上限而失败；后者得到有效的 2 m/s。时长为 0 仍应走原来的非法输入分支。

    **放在哪里**：这是 speed 内的插入片段；调用者仍须先检查 expected 的成功状态。

    ```cpp
    // 放在 result 已检查有限之后，成功返回之前。
    if (result > 2.0) {
        return std::unexpected(std::string{"speed limit exceeded"});
    }
    ```

    **核对这段修改的结果**：

    | 调用 | 应有结果 |
    | --- | --- |
    | `speed(4.0, 1.0)` | 失败，原因是 speed limit exceeded |
    | `speed(4.0, 2.0)` | 成功，速度为 2 m/s |

</div>


## 延伸阅读

[规范或官方指南](https://eel.is/c++draft/expected)。标准草案会继续更新，查阅时注意条款可能包含晚于本章示例的功能。


---

[返回学习路线](index.md) · [上一章：11 · C++20：概念、范围与 span](cpp20.md) · [下一章：13 · 并发与线程 →](concurrency.md)
