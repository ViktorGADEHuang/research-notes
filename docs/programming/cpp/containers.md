# 05 · 容器与标准算法

**示例标准：C++17**

容器负责装数据，算法负责处理数据。优先组合标准库工具，通常比自己维护数组容量和排序循环更容易检查。


!!! tip "读完这页，你应该能做到"

    选出合适容器，分清元素数量、容量和末尾迭代器。

    **先会这些就够了**：循环、函数。


## 看图梳理

![容器装数据，算法做处理](../../assets/learning/cpp-containers.svg){ .learning-figure }

[打开大图](../../assets/learning/cpp-containers.svg)

**选择容器**：动态列表：vector，固定数量：array；**调用算法**：排序、筛选、累加，区间是 [begin, end)；**注意边界**：end 不能解引用，扩容可能使引用失效。


## 列表与算法各负责哪一半

想象一份距离清单 {4, 1, 3, 2}：vector 负责保存这四个数，sort 负责重新排列，count_if 负责计数，accumulate 负责求和。选择不同算法，仍可以处理同一份清单。

`begin()` 与 `end()` 给出要处理的区间。end 不是最后一个元素，而是最后一个元素后面的位置；从 begin 开始，处理到 end 之前就停。这让空列表也能用 begin == end 表示。

| 操作 | 输入是否改变？ | 得到什么 |
| --- | --- | --- |
| sort | 会，顺序变成 1、2、3、4 | 原列表被排序 |
| count_if：小于等于 2 | 不会 | 数量 2 |
| accumulate：初值 0.0 | 不会 | 总和 10.0 |

count_if 需要一条“算不算”的规则。下面 `[](double d) { return d <= 2.0; }` 就是这样的短函数：读一个距离，返回 true 或 false。这里先会看懂这条规则，捕获变量等细节留到第 08 章。


## 先选合适的容器

| 容器 | 适合的场景 | 注意 |
| --- | --- | --- |
| `std::vector<T>` | 数量会变化的连续列表 | 扩容可能使旧引用和指针失效 |
| `std::array<T, N>` | 编译时知道固定数量 | 大小是类型的一部分 |
| `std::map<K, V>` | 按键查找，并按键有序遍历 | 通常查找为对数复杂度 |
| `std::unordered_map<K, V>` | 按键快速查找，不要求顺序 | 平均常数查找，最坏可线性 |

迭代器像指向容器元素的位置标记。`begin()` 指向起点，`end()` 指向末尾之后，不能解引用。常见算法使用半开区间 `[begin, end)`。

## 完整示例

```cpp
#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>

// 程序入口；下面按顺序执行示例步骤。
int main() {
    std::vector<double> distances{4.0, 1.0, 3.0, 2.0};
    // 对半开区间 [begin, end) 排序，修改原容器。
    std::sort(distances.begin(), distances.end());
    // 统计满足条件的元素，不生成另一个列表。
    const auto close_count = std::count_if(
        distances.begin(), distances.end(),
        // 无捕获 Lambda：每个距离小于等于 2 才算接近。
        [](double d) { return d <= 2.0; });
    // 初值 0.0 让累加保持浮点类型。
    const double sum = std::accumulate(
        distances.begin(), distances.end(), 0.0);
    for (const auto distance : distances) {
        std::cout << distance << ' ';
    }
    std::cout << "\nclose: " << close_count << ", sum: " << sum << '\n';
    // at 带范围检查，非法位置会抛异常。
    std::cout << "first: " << distances.at(0) << '\n';
}
```

## 编译与运行

在示例目录执行。Windows 使用 PowerShell；Linux/macOS 将 `./containers.exe` 换成 `./containers`，并把输出文件名的 `.exe` 去掉。

```powershell
g++ -std=c++17 -Wall -Wextra -Wpedantic containers.cpp -o containers.exe
./containers.exe
```

预期输出：

```text
1 2 3 4 
close: 2, sum: 10
first: 1
```

## 怎样读这段代码

`sort` 修改原列表，把距离从小到大排列；`count_if` 对每个元素执行条件函数，统计满足条件的数量；`accumulate` 从 `0.0` 开始求和。

`[](double d) { return d <= 2.0; }` 是一个就地写出的短函数，第 08 章会详细讲 Lambda。

`at(0)` 带越界检查，访问非法位置会抛 `std::out_of_range`；`operator[]` 在本教程的 C++17/20/23 示例中不提供这种异常检查，越界属于未定义行为。

## 常见错误

- `reserve(100)` 只预留容量，不会产生 100 个元素；`resize(100)` 才改变元素数量。
- 不要在范围循环里随意 `push_back` 到正在遍历的 `vector`。
- `map[key]` 在键不存在时会插入默认值；只想查询时使用 `find`，或在 C++20 用 `contains`。

## 动手练习

<div class="practice-card" markdown="1">

<p class="practice-kicker">接着正文做一个小改动</p>

<p class="practice-title">从同一份列表得到两种统计</p>

排序不只是输出好看。标准算法还能帮助你回答“有几只较远、最远距离是多少”。

**从哪里开始**：使用 containers.cpp 中原来的 distances 列表，替换 main 中的统计与输出部分。

**按这几步做**：

1. 用 count_if 统计严格大于 2 米的元素。
2. 用 max_element 找最大值。
3. 先检查返回值不是 end，再解引用。

??? tip "需要一点提示？"

    最大元素迭代器是一个位置，不是数值；空列表时它等于 end。

??? example "查看参考修改与解释"

    原列表为 {4, 1, 3, 2}，大于 2 的有两个，最大为 4。即使以后输入变成空列表，下面的判断也避免了解引用 end。

    **放在哪里**：放在 main 的 distances 声明之后；替换原来的排序、统计和输出演示。

    ```cpp
    const auto far_count = std::count_if(
        distances.begin(), distances.end(),
        [](double distance_m) { return distance_m > 2.0; });
    const auto farthest = std::max_element(distances.begin(), distances.end());
    std::cout << "far count: " << far_count << '\n';
    if (farthest != distances.end()) {
        std::cout << "max distance: " << *farthest << '\n';
    } else {
        std::cout << "no distances\n";
    }
    ```

    **核对这段修改的结果**：

    ```text
    far count: 2
    max distance: 4
    ```

</div>


## 延伸阅读

[规范或官方指南](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)。标准草案会继续更新，查阅时注意条款可能包含晚于本章示例的功能。


---

[返回学习路线](index.md) · [上一章：04 · 类与 RAII](classes.md) · [下一章：06 · 指针与智能指针 →](ownership.md)
