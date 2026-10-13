# 11 · C++20：概念、范围与 span

**示例标准：C++20**

C++20 让类型要求更清楚，让数据处理更像描述步骤。concepts 限制“谁能调用”，ranges 组织“怎么处理”，span 表示“借用哪一段”。


!!! tip "读完这页，你应该能做到"

    分别说出 concepts、ranges、span 解决什么问题。

    **先会这些就够了**：模板、Lambda、容器。


## 看图梳理

![C++20 的三个常用工具](../../assets/learning/cpp-cpp20.svg){ .learning-figure }

[打开大图](../../assets/learning/cpp-cpp20.svg)

**谁能调用**：concepts，编译期检查类型要求；**怎样处理**：ranges / views，延迟筛选与转换；**借用哪一段**：span，连续数据 + 长度。


## 三个新工具不要混成一种东西

下面程序有三件独立的事：换算米到厘米、筛选较远距离、求平均。concepts 检查允许传入的类型；ranges/views 描述筛选步骤；span 把已有连续数据借给函数。

| 距离输入 | 大于 2 米？ | 筛选后换算 |
| --- | --- | --- |
| 1 米 | 否 | 不输出 |
| 3 米 | 是 | 300 厘米 |
| 5 米 | 是 | 500 厘米 |

管道符 `|` 在这段范围代码里连接处理规则，可以读成“先筛选，再转换”。view 通常在遍历时才实际做处理；定义 far_cm 时，并不是已经生成了新的 {300, 500} 列表。

mean 借到的是原始三个距离，所以平均是 (1 + 3 + 5) / 3 = 3 米，不能拿筛选后的两个厘米数来解释它的输出。span 保存长度，却不负责让源 vector 活得更久。


## 三个功能解决三个问题

**Concepts（概念）**是编译期类型约束。`std::floating_point T` 要求 `T` 是浮点类型，传整数会在编译期被拒绝。概念能检查语法或类型要求，不能证明单位、业务逻辑和数值精度正确。

**Ranges（范围）**把一段可遍历的数据作为整体。`views::filter` 筛选，`views::transform` 转换，管道 `|` 将步骤组合。很多 view 延迟到遍历时才算，并没有立即创建新容器。

**span** 借用连续内存，同时保存元素数量，不拥有数据。`span<const double>` 不能通过它修改元素；原数据仍必须有效。它并不是自动管理生命周期的智能指针。

## 先用你熟悉的循环表达同一个任务

在完整程序 main 内创建 distances 之后，下面这段可以替代 far_cm 管道和相应输出循环。先理解普通循环，再把相同意图写成 views：

```cpp
for (double distance_m : distances) {
    if (distance_m > 2.0) {             // 第一步：不够远就跳过。
        const double distance_cm = distance_m * 100.0; // 第二步：换算单位。
        std::cout << distance_cm << ' '; // 依次输出 300 和 500。
    }
}
std::cout << '\n';
```

views 版本把“取哪些”和“怎样变换”分别写成 filter 与 transform。这不是另一套数学，筛选条件、换算公式和输出顺序都能用上面的循环解释。管道符在这里被库定义为组合操作，离开这个语境不要把所有 `|` 都理解为数据处理管道。

## 延迟计算：没有遍历，就还没有结果列表

本例定义 far_cm 后，尚未建立一份拥有 300、500 的新 vector。遍历它时，底层的数据会按筛选与转换规则被访问。得到的是一种访问方式，生命周期仍与原 distances 有关系。filter_view 对某些底层范围会缓存起点，因此“延迟”也不等于修改原数据后每次都必然从头重算。

所以不要在生成 view 后随意改变原容器结构，也不要把依赖局部 vector 的 view 返回到函数外继续使用。若任务要求保存一份独立结果，可以显式遍历并逐项放进新的 vector；“view”与“独立存储”需要按实际用途选择。

## span 为什么不是另一种 vector

| 问题 | vector | 本章的 span |
| --- | --- | --- |
| 谁保管元素存储 | 容器自己 | 原数组或容器 |
| 是否知道元素数量 | 是 | 是 |
| 能不能 push_back | 可以 | 不可以，它只描述已有一段 |
| 源数据销毁后还能否使用 | 自己销毁前通常仍拥有数据 | 不可以，借用已经失效 |

`mean(std::span<const double> values)` 的 const 在 double 前，表示不通过该 span 修改元素。若写 `const std::span<double>`，限制的是 span 对象本身，并不等于把 double 元素变成只读；初学表示只读输入时选前一种写法。

## concepts 拒绝的是类型，不是“不好的数值”

`meters_to_centimeters(3.0)` 推导 T 为 double，满足 floating_point；`meters_to_centimeters(3)` 推导 T 为 int，所以约束不满足，不能靠“3 也能表示米”蒙混过去。显式用小数表达输入，是此示例接口的要求。

反过来，double 类型的 −3.0、NaN、无穷大仍然满足 floating_point。concepts 不会自动检查距离非负或单位是否是米；本例只演示类型约束、普通有限数的转换与均值。mean 只检查空输入，遇到异常测量值还需另外验证。

## 把数组的一部分借给函数，先检查数量

span 可以借用 vector，也可以借用数组。下面片段放在完整程序的 main 内，mean 的定义与头文件保持原样；first(2) 的含义是“借前两个元素”：

```cpp title="main 内片段 · 安全选择前两个测量值"
const double readings[]{2.0, 4.0, 9.0}; // 三个连续存放的 double。
const std::span<const double> all{readings}; // 借用整段，不复制元素。
if (all.size() >= 2) { // first(2) 需要至少两个元素，不自动代你验证。
    const auto first_two = all.first(2); // 仍然借用 readings 的前两个数。
    std::cout << "first two mean: " << mean(first_two) << '\n'; // (2+4)/2=3。
}
```

输出为 `first two mean: 3`。all 与 first_two 都只是借用，readings 是实际的数据；它在当前作用域里活着，所以此处调用有效。span 有长度，便于函数知道范围，但 first 和下标仍有使用前提，见 [子范围的标准约定](https://eel.is/c++draft/span.sub)；本章 C++20 不提供 span::at。

这段是**数值列表的切片**，没有筛选，也没有换算单位。与前面的 view 管道分开追踪，先说明每份对象是数据还是访问方式，再组合到复杂程序中。

## 完整示例

```cpp title="cpp20.cpp · 完整示例"
#include <concepts>
#include <iostream>
#include <ranges>
#include <span>
#include <stdexcept>
#include <vector>

// concepts 约束 T 为浮点类型，整数调用会被拒绝。
template<std::floating_point T>
T meters_to_centimeters(T meters) {
    // T{100} 将 100 写成同一个浮点类型；这里仍由调用方保证单位是米。
    return meters * T{100};
}

// 借用连续数据并带长度，不拥有数据，也不延长生命周期。
double mean(std::span<const double> values) {
    if (values.empty()) {
        // 输入不符合函数约定，报告原因而不继续计算。
        throw std::invalid_argument("empty samples");
    }
    double total{0.0};
    // 先累计原始距离，再除以数量；并未对筛选后的厘米结果求平均。
    for (double value : values) { total += value; }
    return total / static_cast<double>(values.size());
}

// 程序入口；下面按顺序执行示例步骤。
int main() {
    const std::vector<double> distances{1.0, 3.0, 5.0};
    // view 保存处理规则，不立即生成结果列表；不能盲目声明为 const。
    auto far_cm = distances
        // 保留大于 2 米的元素，遍历时筛选。
        | std::views::filter([](double d) { return d > 2.0; })
        // 把筛选后的米转换为厘米，遍历时计算。
        | std::views::transform([](double d) { return meters_to_centimeters(d); });
    // 开始遍历才触发延迟筛选与转换。
    for (double value : far_cm) {
        std::cout << value << ' ';
    }
    // 这里传原来的 vector，隐式建立只读 span，元素并未被复制一份。
    std::cout << "\nmean: " << mean(distances) << '\n';
}
```

## 编译与运行

把上面的完整程序保存为 `cpp20.cpp`，在保存这个文件的目录打开终端。短片段与练习修改不要额外拼在完整程序后面；按正文标明的位置替换或追加。Windows 使用 PowerShell；Linux/macOS 将 `./cpp20.exe` 换成 `./cpp20`，并把输出文件名的 `.exe` 去掉。

```powershell
g++ -std=c++20 -Wall -Wextra -Wpedantic cpp20.cpp -o cpp20.exe
./cpp20.exe
```

预期输出：

```text
300 500 
mean: 3
```

## 怎样读这段代码：先过滤和换算，再对原数据求平均

本例有两条处理路线。far_cm 过滤并换算，最后输出厘米；mean 则直接读取原始距离，计算米制平均值。它们没有共用一份新生成的结果列表。

| 原始距离 | filter 的 d > 2 | transform 是否执行 | 输出 |
| --- | --- | --- | --- |
| 1 米 | false | 不执行 | 跳过 |
| 3 米 | true | 调用 meters_to_centimeters，乘 100 | 300 厘米 |
| 5 米 | true | 调用 meters_to_centimeters，乘 100 | 500 厘米 |

管道里的 `|` 可读成“接着应用这个处理规则”。建立 far_cm 时主要保存访问关系和规则，范围 for 遍历它时才为需要的元素进行处理。它不是一个已经独立保存 {300, 500} 的 vector。底层 distances 和规则依赖的数据需要在使用期间有效。

接着 mean(distances) 建立只读 span，借看原来的 {1, 3, 5}，总和 9、数量 3，得到 3 米。span 同时携带数据访问与长度，既不负责清理 vector 的内存，也不会因为传给函数就复制全部元素。

### concepts 为什么只能检查部分要求？

`std::floating_point T` 要求 T 是浮点类型，所以用 double 的 3.0 可以调用，用 int 的 3 会被拒绝。它看的是类型，不会确认这个 3.0 真的是米，也不会替你拒绝 NaN。代码中的类型条件、单位约定、数据有效性检查，仍各有各的职责。

理解现代工具时可以先写熟悉的 for，再对照 filter、transform、span 分别省去了哪种重复工作。复杂语法应服务于清楚的数据流程，不必为了使用新版本就把能读懂的简单逻辑藏起来。

## 常见错误

- 不要返回依赖局部容器的 view，离开函数后底层数据会销毁。
- 本例的 view 不能声明为 const：filter_view 的遍历可能更新内部缓存，const 底层数据和 const view 是不同的限制。
- view 不是必然更快；实际性能需要测量。
- 本章标准的 span 下标访问没有 `at()` 异常检查，不要把“带长度”误解成“自动防越界”。

## 动手练习

<div class="practice-card" markdown="1">

<p class="practice-kicker">接着正文做一个小改动</p>

<p class="practice-title">只替换数据处理的一步</p>

正文用 filter 筛选，再用 transform 将米换成厘米。这次保留管道结构，改成筛选后求距离的平方。

**从哪里开始**：在 cpp20.cpp 的 main 中，替换原 far_cm 定义与其输出循环，保留原始 distances。

**按这几步做**：

1. 把筛选条件改成 d >= 3.0。
2. 把转换规则改成 d * d，结果单位为平方米。
3. 用纸笔解释为什么整数 3 不能通过 floating_point 约束。

??? tip "需要一点提示？"

    不要让结果继续叫 far_cm，因为它不再是厘米；名字也要随含义更新。

??? example "查看参考修改与解释"

    列表 {1, 3, 5} 留下 3 和 5，再平方得到 9 和 25。meters_to_centimeters(3) 的整数类型不满足约束；3.0 是浮点类型。

    **放在哪里**：替换原管道和遍历循环；保留非 const 的 view 变量，原 mean 输出可继续保留。

    ```cpp
    auto squared_distances = distances
        | std::views::filter([](double d) { return d >= 3.0; })
        | std::views::transform([](double d) { return d * d; });
    for (double value : squared_distances) {
        std::cout << value << ' ';
    }
    std::cout << '\n';
    ```

    **核对这段修改的结果**：只看新增或替换部分的输出；保留的正文演示可能还有其他输出。

    ```text
    9 25
    ```

</div>


## 延伸阅读

[规范或官方指南](https://eel.is/c++draft/range.adaptors)。标准草案会继续更新，查阅时注意条款可能包含晚于本章示例的功能。


---

[返回学习路线](index.md) · [上一章：10 · C++17 常用工具](cpp17.md) · [下一章：12 · C++23：用 expected 表达失败 →](cpp23.md)
