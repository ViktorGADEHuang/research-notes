# 10 · C++17 常用工具

**示例标准：C++17** · [下载完整代码](examples/cpp17.cpp)

C++17 有一批实用工具，让接口更准确地表达“可能没有结果”“几种结果之一”和“只读地看一段文字”。

## 四个先学会的功能

| 功能 | 通俗解释 | 重点 |
| --- | --- | --- |
| `std::optional<T>` | 可能有 T，也可能没有 | 空结果不同于数值 0 |
| `std::variant<A, B>` | 当前保存其中一种类型 | 用 `visit` 或 `get_if` 处理 |
| 结构化绑定 | 将组合结果拆成命名变量 | `const auto& [key, value]` 可避免复制 |
| `std::string_view` | 借看文字，不拥有文字 | 原文字必须仍然有效 |

`std::filesystem` 也在 C++17 中进入标准库，可操作路径、遍历目录；文件操作可能失败，需处理异常或 `error_code`。本章先把没有值与字符串借用讲清。

## 完整示例

```cpp
#include <iostream>
#include <map>
#include <optional>
#include <string>
#include <string_view>
#include <variant>

std::optional<double> lookup(const std::map<int, double>& positions, int id) {
    if (const auto it = positions.find(id); it != positions.end()) {
        return it->second;
    }
    return std::nullopt;
}

int main() {
    const std::map<int, double> positions{{1, 0.0}, {2, 3.5}};
    for (const auto& [id, x] : positions) {
        std::cout << "sheep " << id << ": " << x << '\n';
    }
    std::cout << "missing fallback: " << lookup(positions, 9).value_or(-1.0) << '\n';
    if (auto x = lookup(positions, 1)) {
        std::cout << "valid zero: " << *x << '\n';
    }
    const std::string name{"herding"};
    const std::string_view view{name};
    std::cout << "view: " << view << '\n';
    const std::variant<int, std::string> message{std::string{"ready"}};
    std::visit([](const auto& value) { std::cout << value << '\n'; }, message);
}
```

## 编译与运行

在示例目录执行。Windows 使用 PowerShell；Linux/macOS 将 `./cpp17.exe` 换成 `./cpp17`，并把输出文件名的 `.exe` 去掉。

```powershell
g++ -std=c++17 -Wall -Wextra -Wpedantic cpp17.cpp -o cpp17.exe
./cpp17.exe
```

预期输出：

```text
sheep 1: 0
sheep 2: 3.5
missing fallback: -1
valid zero: 0
view: herding
ready
```

## 怎样读这段代码

`optional` 的真假表示有没有值，不是里面的数字是不是 0。所以查询编号 1 的位置 0.0 仍然成功。`value_or` 在缺失时使用默认值，但实际业务别用容易与正常数据混淆的哨兵值作为唯一错误机制。

带初始化语句的 `if` 把迭代器的使用范围限制在这个判断里。结构化绑定把键值对拆成 `id` 和 `x`。

`string_view` 依赖 `name` 的存储。本例先创建 `name`，后创建 `view`，使用时原字符串未被销毁或改动到使存储失效。`visit` 根据 variant 当前类型调用同一 Lambda。

## 常见错误

- 对空 `optional` 直接 `*value` 不安全，先检查；`value()` 在无值时会抛异常。
- 不要返回指向局部 `std::string` 的 `string_view`；也不要把临时字符串的 view 长期保存。
- `string_view` 不保证以空字符结尾；向需要 C 字符串的接口传 `data()` 前必须检查接口要求。

## 动手练习

查询编号 2 和 3，分别输出值或 missing，不用 -1 替代缺失值。

??? tip "展开参考答案"

    ```cpp
    for (int id : {2, 3}) {
        if (auto x = lookup(positions, id)) {
            std::cout << *x << '\n';
        } else {
            std::cout << "missing\n";
        }
    }
    // 输出 3.5，然后 missing。
    ```

## 延伸阅读

[规范或官方指南](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)。标准草案会继续更新，查阅时注意条款可能包含晚于本章示例的功能。


---

[返回学习路线](index.md) · [上一章：09 · 移动语义](move.md) · [下一章：11 · C++20：概念、范围与 span →](cpp20.md)
