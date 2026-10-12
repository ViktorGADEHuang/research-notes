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

## 先会放入和取出一个元素，再谈算法

下面片段放在 main 内，文件需要 `<vector>` 和 `<iostream>`。它独立于后面完整示例的 distances 列表，用 readings 避免同名：

```cpp
std::vector<double> readings{1.2, 2.8}; // 现在有两个元素，下标为 0 和 1。
readings.push_back(4.0);               // 在末尾再放一个，现在有三个元素。
std::cout << readings.size() << '\n';  // 输出 3，size 是已有元素数量。
std::cout << readings.at(0) << '\n';   // 输出 1.2，下标从 0 开始。
readings.at(1) = 3.0;                  // 修改已有的第二个元素，不改变数量。
```

**下标**是元素的位置编号，与羊的身份编号没有关系。三只羊的身份可以是 7、18、42，但把它们放进 vector 后，三个位置仍然是 0、1、2。要按身份找记录，可以另外使用 map；不要把身份编号直接当作 vector 下标。

### size 与 capacity 不是一回事

size 像已经坐下的人数，capacity 像目前准备好的座位数量。`reserve(100)` 只为容器预留空间，现有元素数量不变，不能因此访问第 99 个元素；`resize(100)` 才把元素数量改为 100。新增 double 元素通常由这种 resize 写法初始化为 0.0。

vector 扩容时可能换到更大的存储区域。此前保存的元素指针、引用、迭代器就可能失效；“变量还在作用域内”不等于“它借用的那个位置还有效”。初学先完成增删，再开始遍历，避免一边走列表一边改变其布局。

## 算法接收的不是数字下标，而是一段区间

把排序后的列表画成位置关系：

```text
元素：      1.0    2.0    3.0    4.0    [没有元素]
下标：       0      1      2      3
位置：     begin()                         end()
处理范围：   └────────包含这四个元素──────────┘
```

这就是 `[begin, end)` 中“左边包含、右边不包含”的意思。`std::max_element` 返回的是其中一个**位置**，写 `*位置` 才读到那个数；空列表没有最大元素，返回 end，此时不能加星号读取。

`count_if` 的 if 不是要你给它一条写死的 if 语句，而是要你提供一个可被调用的判断规则。本例对 1、2、3、4 分别判断 `d <= 2.0`，得到 true、true、false、false，所以计数是 2。算法不用知道“羊”是什么，它只按规则处理每个 double。

`sort` 需要元素之间有合适的顺序关系；本例使用有限普通距离。包含 NaN 的浮点测量值应先按业务要求拒绝或处理，不能拿本例直接声称完成了任意传感器数据的稳健排序。

## 完整示例

```cpp
#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>

// 程序入口；下面按顺序执行示例步骤。
int main() {
    // 四个元素的下标为 0、1、2、3；size() 是元素数量 4。
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
    // 排序后逐项读取；这里只输出数值，不需要修改元素或复制整个容器。
    for (const auto distance : distances) {
        std::cout << distance << ' ';
    }
    std::cout << "\nclose: " << close_count << ", sum: " << sum << '\n';
    // 本例确定非空，at(0) 取第一个元素；若下标越界，at 会抛异常。
    std::cout << "first: " << distances.at(0) << '\n';
}
```

## 编译与运行

把上面的完整程序保存为 `containers.cpp`，在保存这个文件的目录打开终端。短片段与练习修改不要额外拼在完整程序后面；按正文标明的位置替换或追加。Windows 使用 PowerShell；Linux/macOS 将 `./containers.exe` 换成 `./containers`，并把输出文件名的 `.exe` 去掉。

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
