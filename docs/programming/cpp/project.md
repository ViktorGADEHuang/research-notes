# 15 · 放牧场景的数据处理小项目

**示例标准：C++20**

把前面知识串起来：输入一帧羊的位置，检查数据，算羊群中心和最远的羊。这个程序用于练习数据处理接口，不直接生成机器人控制指令。


!!! tip "读完这页，你应该能做到"

    手算一帧数据的中心与最远个体，检查无效输入。

    **先会这些就够了**：span、optional、容器。


## 看图梳理

![一帧羊的位置怎样变成统计结果](../../assets/learning/cpp-project.svg){ .learning-figure }

[打开大图](../../assets/learning/cpp-project.svg)

**检查数据**：空帧与非有限坐标，编号不可重复；**计算中心**：同一坐标系、单位米，逐项累加再除以数量；**比较距离**：hypot 计算距离，最远者编号与半径。


## 先手算一帧，再把它拆成程序步骤

输入三只羊的位置：(0, 0)、(2, 0)、(4, 3)，都用同一坐标系、单位米。我们先只回答两件事：几何中心在哪里，谁离中心最远？这不是驱赶动作的决策。

| 阶段 | 手算结果 | 程序对应位置 |
| --- | --- | --- |
| 检查输入 | 非空、编号不同、坐标有限 | summarize 开头与第一次循环 |
| 求中心 | x = 6/3 = 2，y = 3/3 = 1 | 累加后除以数量 |
| 比较距离 | 三只约为 2.236、1、2.828 米 | 第二次循环中 hypot |
| 交回结果 | 中心 (2,1)，最远编号 3 | 返回 Summary |

为什么分两次循环？第一次循环结束才知道最终中心，第二次才能对所有羊计算到同一个中心的距离。不能一边用还在变化的中心一边决定最远个体。

`result->center.x_m` 可以一层层读：result 里有统计结果，统计结果中有 center，center 中有 x_m。先确认 optional 有值，才沿这条路径读取。理解数据的层级，比先背整行符号更容易。


## 先把输入和输出说清楚

输入是同一个二维坐标系中的位置，单位米。输出包含中心位置、最远羊的编号、它到中心的距离。这里每只羊权重相同，中心取算术平均。

![从位置到统计结果的处理步骤](assets/pipeline.svg)

`struct` 表示简单数据；`span<const Sheep>` 借用整帧；`optional` 表示“这帧无法得到统计结果”；`hypot(dx, dy)` 计算二维距离。本例拒绝空帧、非有限坐标和重复编号，计算后也检查非有限结果。

## 数据怎么一层层装起来，先不要急着看计算

`struct` 是把相关字段放在一起的一种类型。这里三层含义各不相同：Point 是位置，Sheep 是有身份的位置记录，Summary 是整帧计算结果。

| 写法 | 对应哪份数据 | 可以怎样读 |
| --- | --- | --- |
| `Point{4.0, 3.0}` | 一个位置 | x 为 4 米，y 为 3 米 |
| `Sheep{3, {4.0, 3.0}}` | 一只羊的记录 | 编号 3，位置是上面那个点 |
| `frame[2]` | 列表的第三个位置 | 这次恰好保存编号 3，但下标与编号没有必然关系 |
| `frame[2].position.x_m` | 记录中的位置中的 x | 本例为 4.0 |
| `result->center.x_m` | optional 中 Summary 的中心的 x | 成功时为 2.0，读取前先检查状态 |

花括号按成员声明顺序提供初值。`{3, {4.0, 3.0}}` 的外层是 Sheep，内层是 Point；理解这两层以后，完整输入就只是三条同样格式的记录组成一个 vector。

## 第一遍为什么还要放一个编号集合

容器 unordered_set 只保存不重复的编号。`ids.insert(item.id)` 返回一组信息，其中 second 是“这次是否新插入”：第一次看到编号 7 为 true，再看到 7 为 false。取反后，就能把重复编号当成拒绝条件。

代码使用 `||` 把“x 非有限”“y 非有限”“编号重复”连起来；任何一项成立都退回空 optional。这个运算是短路的，前面条件已成立时后面不必再执行。在本例里发现任何坏坐标就整帧返回，因此不需要再记录这一条编号。

## 第二遍真的比较了哪些数

中心已经确定为 (2, 1) 后，才开始逐个比较到它的距离。减去中心坐标，得到横向差 dx 与纵向差 dy；hypot 用两者算直线距离。

| 编号 | 位置 | dx、dy | 到中心的距离 | 当前最远编号 |
| --- | --- | --- | --- | --- |
| 1 | (0, 0) | −2、−1 | √5，约 2.236 | 1 |
| 2 | (2, 0) | 0、−1 | 1 | 仍为 1 |
| 3 | (4, 3) | 2、2 | √8，约 2.828 | 改为 3 |

`radius_m` 保存已看到的最大距离，不是把所有距离相加。初值 −1 只在函数内部用来确保第一条有效距离能被选中；它不是向调用者返回的“失败半径”。失败路径用 nullopt，成功的半径应非负。

## 检查数据的结果，先写成你能预测的表

| 输入变化 | 为什么这样判断 | 本程序应该怎样回答 |
| --- | --- | --- |
| 一只羊在 (2,1) | 中心就是它自身，到中心距离为 0 | 成功，半径 0 |
| 三只不同编号的羊重合 | 三个到中心距离相同 | 成功，选输入中第一只 |
| 两条记录编号相同 | 不能确认是不是把同一只重复算了两次 | 失败，空 optional |
| 一个坐标为 NaN | 无法进行可靠几何计算 | 失败，空 optional |
| 列表为空 | 没有可求平均的对象 | 失败，空 optional |

这些是接口的明确约定，不是编译器帮你猜出的规则。后面的练习就是把表中前三类小改动放进 main，先预测、再对照；不必一上来改计算函数。

### 这份统计还做不到什么

所有坐标都有限仍不代表任意极端输入都能稳健求平均；本例先求和再除，极端值可能让中间和超范围，随后会被有限性检查拒绝。它没有采用专门的高精度或补偿求和，也没有验证坐标系名称、时间戳或定位误差。

三个小数位只是输出格式，不能据此宣称传感器精确到毫米。这个结果可作为后续算法的输入之一；要制定放牧动作，还需要任务约定、环境观测以及运动与安全约束。

## “中心”和“半径”在这份程序里是哪一种？

本页 center 是各位置的**算术平均点**，不是某只羊的位置，也不保证位于某个安全目标区域。radius_m 是“到这个平均点的最大距离”，不是最小包围圆算法得到的最优半径。

例如只看两个点 (0,0) 与 (4,0)，平均点是 (2,0)，最大距离是 2 米；加进第三个点 (0,0)，平均点变成 (4/3,0)，但最远点仍在 (4,0)，距离变成 8/3 米。位置重复可以合法，编号重复则违反本例的记录约定；两个条件不要混淆。

| 容易混淆的词 | 本例实际做了什么 |
| --- | --- |
| 几何中心 | 按每条记录等权求坐标平均，不考虑体重 |
| 最远编号 | 到平均点的计算距离最大，不是离机器人最远 |
| 半径 | 对本帧数据，以平均点为中心可覆盖这些点的最大距离 |
| 平局 | 计算出的 double 距离相等时保留输入中第一个 |

数学上等距的点，在浮点计算中可能有极小差异。当前严格比较以**实际计算结果**为准，不使用模糊的容差排序。真实系统如果需要稳定的平局规则，应先定义误差阈值与编号选择规则，再写进接口与验证例子。

最后，optional 只表示这份函数明确拒绝的输入没有得到统计值。unordered_set 等容器分配仍可能抛异常，这个接口没有承诺 noexcept；不要把 optional 的失败状态当作已经捕获全部系统错误。

## 完整示例

```cpp title="project.cpp · 完整示例"
#include <cmath>
#include <iomanip>
#include <iostream>
#include <optional>
#include <span>
#include <unordered_set>
#include <vector>

// 同一个二维坐标系中的位置，单位米。
struct Point { double x_m; double y_m; };
// 一条个体记录：编号与它的二维位置绑在一起。
struct Sheep { int id; Point position; };
// 统计结果：中心、最远个体编号、到中心的距离。
struct Summary { Point center; int farthest_id; double radius_m; };

// 只读借用一帧，无法统计时返回没有值。
std::optional<Summary> summarize(std::span<const Sheep> sheep) {
    // 一只羊也没有时没有中心，不能继续除以数量。
    if (sheep.empty()) { return std::nullopt; }
    Point center{0.0, 0.0};
    // 用集合检查编号唯一，不依赖数据先排序。
    std::unordered_set<int> ids;
    for (const auto& item : sheep) {
        if (!std::isfinite(item.position.x_m)
            || !std::isfinite(item.position.y_m)
            // insert 的 second 表示是否新插入；重复编号会得到 false。
            || !ids.insert(item.id).second) {
            // 这一帧含有坏坐标或重复编号，整帧拒绝，避免重复计数。
            return std::nullopt;
        }
        // 累加所有 x 坐标，之后除以数量得到平均值。
        center.x_m += item.position.x_m;
        // y 坐标用同样的方法累加。
        center.y_m += item.position.y_m;
    }
    const auto count = static_cast<double>(sheep.size());
    center.x_m /= count;
    center.y_m /= count;
    if (!std::isfinite(center.x_m) || !std::isfinite(center.y_m)) {
        // 极端坐标可能让累加溢出；不把无穷大当作有效中心。
        return std::nullopt;
    }
    // 半径从 -1 开始，即使全部重合也能选出第一个编号。
    Summary result{center, sheep.front().id, -1.0};
    for (const auto& item : sheep) {
        // 用二维坐标差计算欧氏距离。
        const double distance = std::hypot(
            item.position.x_m - center.x_m, item.position.y_m - center.y_m);
        // 坐标相减或距离计算也可能超出数值范围，单独检查这一关。
        if (!std::isfinite(distance)) { return std::nullopt; }
        // 发现更远个体才替换；平局保留输入中先出现的个体。
        if (distance > result.radius_m) {
            result.farthest_id = item.id;
            result.radius_m = distance;
        }
    }
    return result;
}

// 程序入口；下面按顺序执行示例步骤。
int main() {
    // 示例帧，不是实时采集或机器人控制输入。
    const std::vector<Sheep> frame{{1, {0.0, 0.0}}, {2, {2.0, 0.0}}, {3, {4.0, 3.0}}};
    if (const auto result = summarize(frame)) {
        // fixed 与 setprecision(3) 只改变显示，内部计算仍使用 double。
        std::cout << std::fixed << std::setprecision(3);
        std::cout << "center: (" << result->center.x_m << ", "
                  << result->center.y_m << ") m\n";
        std::cout << "farthest id: " << result->farthest_id << '\n';
        std::cout << "radius: " << result->radius_m << " m\n";
    } else {
        std::cout << "invalid frame\n";
    }
    const std::vector<Sheep> empty;
    std::cout << "empty frame accepted: " << std::boolalpha
              << summarize(empty).has_value() << '\n';
}
```

## 编译与运行

把上面的完整程序保存为 `project.cpp`，在保存这个文件的目录打开终端。短片段与练习修改不要额外拼在完整程序后面；按正文标明的位置替换或追加。Windows 使用 PowerShell；Linux/macOS 将 `./project.exe` 换成 `./project`，并把输出文件名的 `.exe` 去掉。

```powershell
g++ -std=c++20 -Wall -Wextra -Wpedantic project.cpp -o project.exe
./project.exe
```

预期输出：

```text
center: (2.000, 1.000) m
farthest id: 3
radius: 2.828 m
empty frame accepted: false
```

## 怎样读这段代码：两次遍历各有一个任务

输入 frame 里有三条 Sheep，每条绑定自己的编号与 Point。summarize 用 span 借看这帧数据，通过 optional 回传“有统计结果”或“这帧不能按约定统计”。

| 阶段 | 对这份 frame 做什么 | 中间结果 |
| --- | --- | --- |
| 空帧检查 | 至少有一只羊才能求平均位置 | 三只，通过 |
| 第一遍遍历 | 检查坐标有限、编号不重复，再累计坐标 | x 总和 6，y 总和 3 |
| 求平均 | 两个总和分别除以数量 3 | center = (2, 1) 米 |
| 第二遍遍历 | 计算每只羊到中心的距离，保留最大者 | 约 2.236、1、2.828 米 |
| 返回结果 | 中心、最远编号、最远距离装进 Summary | 编号 3，半径约 2.828 米 |
| main 输出 | 成功时读取 result 的成员 | 用三位小数显示，内部数值没有因此取整 |

为什么分两遍？一只羊到中心的距离，需要先知道完整中心。处理第一只羊时总和还没包含后两只，不能把临时中心当最终中心给每只羊分别测距。

`ids.insert(item.id).second` 的 second 是“这次是否新插入”的真假值。编号 7 第一次出现返回 true，再次出现返回 false，触发整帧拒绝；集合既不替你保存坐标，也不是要给编号重新排序。

`std::hypot(dx, dy)` 计算二维欧氏距离。这里中心 (2, 1) 与第三只羊 (4, 3) 的差是 (2, 2)，距离约为 2.828。半径初值 −1 让距离 0 的第一只也能成为候选；比较用严格大于，所以距离平局时保留先出现的个体。

### optional 为什么足够做这页演示，真实接口又可能需要更多？

本例空帧、重复编号、非法数值都返回 nullopt，调用者只知道没得到有效 Summary，并不知道具体原因。若要在日志中区分失败，可以设计 expected 或另外携带错误码，但应先写清错误含义。本章先完成几何统计，没有直接执行放牧决策。

## 常见错误

- 不同坐标系的数据不能直接求平均；“都是米”也不意味着坐标系相同。
- 数据陈旧与数据缺失不同，真实接口应保存时间戳。
- optional 没有解释失败原因；练习时可升级为 C++23 expected，保留具体错误。

## 动手练习

<div class="practice-card" markdown="1">

<p class="practice-kicker">接着正文做一个小改动</p>

<p class="practice-title">用边界输入检查统计接口</p>

正文的一帧数据得到正常统计，但真实数据也可能为空、重合或编号重复。先把这些边界情况讲清，再扩展错误报告。

**从哪里开始**：保留 summarize 定义，在 project.cpp 的 main 中增加几个独立测试帧。

**按这几步做**：

1. 先用一只羊判断中心与半径。
2. 用三只同位置、不同编号的羊判断平局规则。
3. 比较重复编号与空帧的返回状态；先不引入 C++23。

??? tip "需要一点提示？"

    只有成功的 optional 才能读取 center 和 radius；失败不是“中心为零”。

??? example "查看参考修改与解释"

    单只羊的中心为自身，半径为 0。重合时半径为 0，并保留输入中第一只的编号。重复编号和空帧都无法生成有效统计。

    **放在哪里**：为便于核对输出，用它替换 main 的演示部分；summarize 和数据类型定义保留。

    ```cpp
    const std::vector<Sheep> one{{7, {2.0, 1.0}}};
    const std::vector<Sheep> same{
        {7, {2.0, 1.0}}, {8, {2.0, 1.0}}, {9, {2.0, 1.0}}};
    const std::vector<Sheep> duplicate{
        {7, {0.0, 0.0}}, {7, {1.0, 0.0}}};
    const std::vector<Sheep> empty;

    if (const auto result = summarize(one)) {
        std::cout << "one radius: " << result->radius_m << '\n';
    }
    if (const auto result = summarize(same)) {
        std::cout << "same farthest: " << result->farthest_id << '\n';
    }
    std::cout << std::boolalpha;
    std::cout << "duplicate accepted: " << summarize(duplicate).has_value() << '\n';
    std::cout << "empty accepted: " << summarize(empty).has_value() << '\n';
    ```

    **核对这段修改的结果**：

    ```text
    one radius: 0
    same farthest: 7
    duplicate accepted: false
    empty accepted: false
    ```

    **进阶选做**：读完 C++23 章节后，可将返回类型改为 expected，分别报告 empty frame、duplicate id 等错误。先完成上面的边界检查，再做接口升级。

</div>


## 延伸阅读

[规范或官方指南](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)。标准草案会继续更新，查阅时注意条款可能包含晚于本章示例的功能。


---

[返回学习路线](index.md) · [上一章：14 · CMake 与调试](tooling.md)
