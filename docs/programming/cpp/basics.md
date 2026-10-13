# 02 · 变量、判断与循环

**示例标准：C++17**

把变量理解成“有名字、有类型的盒子”。类型决定可以放什么，变量名告诉别人这份数据是什么。


!!! tip "读完这页，你应该能做到"

    分清赋值与比较，手算距离计数和整数除法。

    **先会这些就够了**：第一个程序的结构。


## 看图梳理

![处理一组距离](../../assets/learning/cpp-basics.svg){ .learning-figure }

[打开大图](../../assets/learning/cpp-basics.svg)

**输入**：带单位的距离，只读阈值 3 米；**判断与循环**：逐个比较 distance > 3，满足条件才加一；**结果**：输出计数，检查等于阈值的边界。


## 先在纸上处理三只羊，再把步骤写成代码

现在只做一个任务：距离超过 3 米的羊有几只？输入是 1.2、4.5、2.0 米。先把计数设为 0，再依次看三个距离；满足条件才加一。这就是变量、判断与循环一起工作的理由。

| 这一步读到的距离 | 大于 3 吗？ | 处理后的计数 |
| --- | --- | --- |
| 1.2 | 否 | 0 |
| 4.5 | 是 | 1 |
| 2.0 | 否 | 1 |

`std::vector<double>` 可以先读成“装小数的列表”；本章只需要会依次取出元素，第 05 章再讲容器。`for` 每次取一个元素，`if` 决定要不要执行加一。花括号内的语句就是这一块要执行的内容。

计数为什么放在循环前面？它要记住前面已经数过多少。如果每次循环都重新创建并设为 0，就不能累计结果。先用上表推演，再看下面同一个任务的程序，不用一次记住所有标点。


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

## 从一个数开始，把变量的变化看清楚

下面是**阅读片段**：如果想试，把它放进已包含 `<iostream>` 的 main 内，不要另加一套 main。

```cpp
int count{0};             // 创建一个整数变量，初始值为 0。
count = 2;                // 赋值：覆盖旧值，现在 count 为 2。
count = count + 1;        // 先算右边 2 + 1，再把 3 写回左边。
const bool enough{count >= 3}; // 比较：得到 true，不会改变 count。
std::cout << count << '\n';    // 输出 3。
std::cout << std::boolalpha << enough << '\n'; // 输出 true。
```

`count = count + 1` 不是数学方程。它是一条操作指令，右侧先求值、左侧再接收结果。`++count` 是“把 count 增加 1”的简写；这章把它单独写成一句，不需要讨论复杂表达式里的先后顺序。

`int count{0}` 同时做了“创建变量”和“给初始值”两件事；之后的 `count = 2` 只修改已有变量。`const` 的变量必须在创建时确定值，后面不能再通过这个变量赋新值。

## 再让判断和循环接起来

`if (条件) { 要做的事 }` 的条件得到 true 时才执行花括号内语句；false 时跳过。要描述另外一种情况，可接 `else { 另一件事 }`。常见条件先记下面几个：

| 写法 | 人话 | 对 3.0 和阈值 3.0 的结果 |
| --- | --- | --- |
| `distance_m > threshold_m` | 严格大于 | false |
| `distance_m >= threshold_m` | 大于或等于 | true |
| `distance_m == threshold_m` | 两者相等 | true |
| `distance_m != threshold_m` | 两者不相等 | false |

范围循环 `for (const double distance_m : distances_m)` 从冒号右边的列表逐个取值，交给左边的局部变量。每轮执行同一段花括号；列表读完，才接着执行循环后面的输出。这里 `distance_m` 是一个小数副本，修改计数器不会改原距离列表。

也会遇到按次数重复的写法。这段同样放在 main 内，每行注释按实际执行顺序读：

```cpp
// i 从 0 开始；每次先检查 i < 3；本轮结束后再执行 ++i。
for (int i{0}; i < 3; ++i) {
    std::cout << i << '\n'; // 依次输出 0、1、2，不会输出 3。
}
```

| 当前 i | 检查 i < 3 | 这一轮做什么 | 轮末 i |
| --- | --- | --- | --- |
| 0 | true | 输出 0 | 1 |
| 1 | true | 输出 1 | 2 |
| 2 | true | 输出 2 | 3 |
| 3 | false | 退出，不再执行循环体 | 3 |

本章只处理已经给出的有限、非负距离。`double` 可以出现 NaN、无穷大，也可能有舍入误差；“类型是小数”不等于“传感器数据合法”。第 15 章会把输入检查单独做出来。计数只演示三个元素，不把 int 当作无限大的整数。

## 类型转换并不是检查输入

本页的 5 / 2 只在演示整数除法。想得到 2.5，应在**计算之前**让操作数成为小数；计算完才转换，已经来不及了。下面片段放在带 `<iostream>` 的 main 内：

```cpp title="main 内片段 · 转换发生在除法之前还是之后"
const int total{5};
const int count{2}; // 本例固定为 2；真实输入需要先检查不为 0。
const double too_late = static_cast<double>(total / count); // 先算出整数 2。
const double fractional = static_cast<double>(total) / count; // 先把 5 变为 5.0。
std::cout << too_late << '\n';    // 输出 2。
std::cout << fractional << '\n';  // 输出 2.5。
```

`static_cast` 表示明确要求一种转换，**不负责确认数值能安全装进新类型**。后面读取容器的 size 时也一样：不要把可能很大的数量随手转换成 int。数量类型常是无符号整数，不能拿负下标去“凑”它。

“未定义行为”可以先理解成：程序违反了 C++ 的使用条件，标准不再保证结果。对有符号 int，超出范围后继续加一不是可靠的绕回；整数除以 0 也没有合法结果。初学用本页的几个小数练习，不通过制造这些操作观察“会输出什么”。

## 完整示例

```cpp title="basics.cpp · 完整示例"
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
    // 计数器放在循环外，才能记住前面已经数到多少只。
    int far_count{0};
    // 范围循环，每次读取一个距离。
    for (const double distance_m : distances_m) {
        // 严格大于阈值才计数，等于阈值不计入。
        if (distance_m > threshold_m) {
            // 当前这一只满足条件，计数加一。
            ++far_count;
        }
    }
    // << 把右侧内容交给输出流；字符 '\n' 让下一次输出换行。
    std::cout << experiment << '\n';
    std::cout << "far sheep: " << far_count << '\n';
    // 5 / 2 先按整数做除法；5.0 / 2 中有小数，结果才保留小数部分。
    std::cout << "integer: " << 5 / 2 << ", decimal: " << 5.0 / 2 << '\n';
}
```

## 编译与运行

把上面的完整程序保存为 `basics.cpp`，在保存这个文件的目录打开终端。短片段与练习修改不要额外拼在完整程序后面；按正文标明的位置替换或追加。Windows 使用 PowerShell；Linux/macOS 将 `./basics.exe` 换成 `./basics`，并把输出文件名的 `.exe` 去掉。

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

## 怎样读这段代码：先跟着变量走一遍

从 main 的第一句开始。experiment 保存文字，threshold_m 保存 3.0，distances_m 保存三条距离。它们有 const，所以本程序通过这些名字只读取数据。far_count 是需要变化的计数器，先初始化为 0。

| 执行位置 | 正在读取什么 | far_count 的值 | 为什么 |
| --- | --- | --- | --- |
| 循环前 | 还没处理任何距离 | 0 | 初始值代表已数到零只 |
| 第一轮 | distance_m = 1.2 | 0 | 条件 1.2 > 3.0 为假，跳过 if 的花括号 |
| 第二轮 | distance_m = 4.5 | 1 | 条件为真，执行 ++far_count |
| 第三轮 | distance_m = 2.0 | 1 | 条件为假，计数保持原值 |
| 循环结束 | 三个元素都已处理 | 1 | 才输出最终结果，而不是每轮输出 |

范围循环里的 distance_m 是**本轮取出的一个数**，distances_m 是**整份列表**，名字相近但对象不同。`for (const double distance_m : distances_m)` 的冒号可读成“从右边这组数据里，依次取一个给左边”。没有元素时循环体一次也不执行。

`std::cout << "far sheep: " << far_count << '\n';` 先输出标签，再输出计数，再换行。这里的 `<<` 配合 cout 表示输出，和数字左移不是这处代码的读法；`'\n'` 是一个换行字符，`"far sheep: "` 是一段文字。

最后一行还在比较两种除法：`5 / 2` 两边都是 int，向零截断得到 2；`5.0 / 2` 有浮点操作数，得到 2.5。**先做除法，再把结果输出**；事后把整数除法的 2 转成 double，也不能恢复已经丢掉的 0.5。

### 只改一处，先预测结果

若把阈值改为 2.0，仍用严格大于，则只有 4.5 计入，结果仍为 1；若同时把条件改成大于等于，则 2.0 也计入，结果为 2。做练习时先写下“输入变了还是判定规则变了”，避免两个因素一起改后不知道结果为何变化。

## 常见错误

- 局部 int、double 等变量先给初值；在赋值之前读取未初始化变量不可以当作获得一个随机数。
- `if (distance_m = threshold_m)` 修改了变量，不是比较；编译器警告值得认真看。
- 不要直接用 `double` 的 `==` 判断复杂计算结果相等，应根据单位与误差要求选容差。

## 动手练习

<div class="practice-card" markdown="1">

<p class="practice-kicker">接着正文做一个小改动</p>

<p class="practice-title">边界上的 3 米，到底算不算远</p>

正文只统计大于阈值的距离。现在加入刚好等于阈值的样本，看看一个符号怎样改变结果。

**从哪里开始**：在 basics.cpp 的 main 中改距离列表；比较条件分别使用 > 和 >=。

**按这几步做**：

1. 把 distances_m 改成 {3.0, 3.1, 8.0}。
2. 先在纸上分别标记满足 > 3 和 >= 3 的元素。
3. 用两个计数器保存结果，其他输入保持相同。

??? tip "需要一点提示？"

    3.0 不大于 3.0，但大于等于 3.0；不要把两种任务定义混在一起。

??? example "查看参考修改与解释"

    严格大于时只统计 3.1 和 8.0，得到 2；包含边界时还统计 3.0，得到 3。

    **放在哪里**：替换 main 内的数据、计数与输出部分；头文件保持原样。

    ```cpp
    const double threshold_m{3.0};
    const std::vector<double> distances_m{3.0, 3.1, 8.0};
    int greater{0};
    int greater_or_equal{0};
    for (const double distance_m : distances_m) {
        if (distance_m > threshold_m) { ++greater; }
        if (distance_m >= threshold_m) { ++greater_or_equal; }
    }
    std::cout << "greater: " << greater << '\n';
    std::cout << "greater or equal: " << greater_or_equal << '\n';
    ```

    **核对这段修改的结果**：

    ```text
    greater: 2
    greater or equal: 3
    ```

</div>


## 延伸阅读

[规范或官方指南](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)。标准草案会继续更新，查阅时注意条款可能包含晚于本章示例的功能。


---

[返回学习路线](index.md) · [上一章：01 · 环境与第一个程序](setup.md) · [下一章：03 · 函数、引用与 const →](functions.md)
