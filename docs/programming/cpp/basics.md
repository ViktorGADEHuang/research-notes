# 02 · 变量、判断与循环

**示例标准：C++17** · [下载完整代码](examples/basics.cpp)

把变量理解成“有名字、有类型的盒子”。类型决定可以放什么，变量名告诉别人这份数据是什么。


## 看图梳理

![处理一组距离](../../assets/learning/cpp-basics.svg){ .learning-figure }

[打开大图](../../assets/learning/cpp-basics.svg)

**输入**：带单位的距离，只读阈值 3 米；**判断与循环**：逐个比较 distance > 3，满足条件才加一；**结果**：输出计数，检查等于阈值的边界。


## 先认识几个基本工具

| 写法 | 通俗解释 | 例子 |
| --- | --- | --- |
| `int` | 整数 | 羊的数量 |
| `double` | 带小数的数 | 距离，单位米 |
| `bool` | 是或否 | 是否到达目标 |
| `std::string` | 一段文字 | 实验名称 |
| `const` | 初始化后不再修改 | 距离阈值 |
| `if` | 满足条件才执行 | 羊群太远就提示 |
| `for` | 重复处理一组数据 | 依次检查距离 |

`=` 是赋值，`==` 是比较。`{}` 划出一段代码的作用域；局部变量通常只在所在作用域内可见。用花括号初始化可以拒绝一些缩窄转换，例如 `int n{2.5};` 会编译失败。

`auto` 让编译器从初始值推导类型，不是让变量随时换类型。`auto n = 3;` 的类型仍然是 `int`。

## 完整示例

```cpp
#include <iostream>
#include <string>
#include <vector>

// 程序入口；下面按顺序执行示例步骤。
int main() {
    // 实验名初始化后不修改。
    const std::string experiment{"herding-demo"};
    // 距离阈值，单位米；用名字说明物理含义。
    const double threshold_m{3.0};
    // 列表拥有三个距离元素，数量由容器管理。
    const std::vector<double> distances_m{1.2, 4.5, 2.0};
    int far_count{0};
    // 范围循环，每次读取一个距离。
    for (const double distance_m : distances_m) {
        // 严格大于阈值才计数，等于阈值不计入。
        if (distance_m > threshold_m) {
            // 当前这一只满足条件，计数加一。
            ++far_count;
        }
    }
    // 把结果输出到终端，便于与正文中的示例结果对照。
    std::cout << experiment << '\n';
    // 把结果输出到终端，便于与正文中的示例结果对照。
    std::cout << "far sheep: " << far_count << '\n';
    // 把结果输出到终端，便于与正文中的示例结果对照。
    std::cout << "integer: " << 5 / 2 << ", decimal: " << 5.0 / 2 << '\n';
}
```

## 编译与运行

在示例目录执行。Windows 使用 PowerShell；Linux/macOS 将 `./basics.exe` 换成 `./basics`，并把输出文件名的 `.exe` 去掉。

```powershell
g++ -std=c++17 -Wall -Wextra -Wpedantic basics.cpp -o basics.exe
./basics.exe
```

预期输出：

```text
herding-demo
far sheep: 1
integer: 2, decimal: 2.5
```

## 怎样读这段代码

距离列表中只有 `4.5` 大于 `3.0`，所以计数是 1。范围 `for` 每次取一个距离；`++far_count` 把计数加一。

`5 / 2` 的两个操作数都是整数，结果是整数 2；只要有一个操作数是浮点数，就按浮点除法计算。`std::cout` 把右侧内容依次输出，`'\n'` 表示换行。

`#include` 引入声明，`std::` 表示标准库命名空间，`main` 是程序入口。

## 常见错误

- 未初始化的局部基本类型变量可能包含不确定的值，先给初值。
- `if (distance_m = threshold_m)` 修改了变量，不是比较；编译器警告值得认真看。
- 不要直接用 `double` 的 `==` 判断复杂计算结果相等，应根据单位与误差要求选容差。

## 动手练习

把距离改成 `{3.0, 3.1, 8.0}`。严格“大于 3 米”与“大于等于 3 米”分别得到多少？

??? tip "展开参考答案"

    `>` 得到 2；`>=` 得到 3。边界是否算进去由任务定义决定，不是语法帮你决定。

## 延伸阅读

[规范或官方指南](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)。标准草案会继续更新，查阅时注意条款可能包含晚于本章示例的功能。


---

[返回学习路线](index.md) · [上一章：01 · 环境与第一个程序](setup.md) · [下一章：03 · 函数、引用与 const →](functions.md)
