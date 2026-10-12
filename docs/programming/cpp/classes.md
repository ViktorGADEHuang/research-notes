# 04 · 类与 RAII

**示例标准：C++17**

类把相关数据和操作放到一起。RAII 的直觉是：让对象替你保管资源，对象离开作用域时自动归还。资源可以是内存、文件、锁，也可以是设备连接。


!!! tip "读完这页，你应该能做到"

    解释构造检查和成员自动清理为什么能减少资源错误。

    **先会这些就够了**：函数、const。


## 看图梳理

![类怎样维持合法状态](../../assets/learning/cpp-classes.svg){ .learning-figure }

[打开大图](../../assets/learning/cpp-classes.svg)

**构造时**：初始化成员，拒绝非法速度；**使用时**：公开受控接口，只读操作加 const；**销毁时**：成员自动析构，资源跟随生命周期。


## 类：把一份数据和允许的操作放在一起

单独用一个 double 保存速度，任何代码都可能把它改成 −1。类让我们把速度藏在 private 区域，只通过设计好的接口使用。这像一份带规则的数据记录：创建时检查规则，之后不开放随意改写的入口。

`Robot` 是类型，也就是这份记录的格式；`robot` 是按这个格式创建的一份具体对象。`Robot{0.8}` 会调用构造函数，保存 0.8 米/秒。`robot.distance(5.0)` 调用该对象的成员函数，以保存的速度算 5 秒的距离：0.8 × 5 = 4 米。

| 时刻 | 程序在做什么 |
| --- | --- |
| 创建对象 | 初始化成员，检查速度是否有效 |
| 调用 distance | 读取速度，检查时间，返回计算结果 |
| 离开作用域 | 销毁对象，其 vector 成员也清理自身资源 |

RAII 是 Resource Acquisition Is Initialization 的缩写；先记住实际用法：**把资源交给会自动清理的对象管理**。不需要初学就手写复杂析构函数。下面的 vector 成员只用来示范资源随对象清理，不代表实现了传感器采集。


## 构造、析构与不变量

**构造函数**在对象创建时执行；**析构函数**在对象正常销毁时执行。私有成员不能被外部代码随意改写。下面的类让“机器人速度必须有限且非负”一直成立，这种要求叫不变量。

![对象的生命周期与资源释放](assets/lifetime.svg)

初学时优先让 `std::vector`、`std::string`、智能指针等现成类型管理资源。这叫 **Rule of Zero**：成员已经会清理，就尽量不自己写析构、复制和移动函数。

`struct` 默认成员公开，`class` 默认成员私有。不是“struct 不能有函数”，而是默认访问权限不同。

## 冒号、下划线和 const，到底各管什么

先看这一行：`explicit Robot(double speed_mps) : speed_mps_{speed_mps}`。它不是普通返回值函数，名字与类名 Robot 相同，叫构造函数，任务是让新对象带着合适的初始数据出现。

| 部分 | 通俗解释 |
| --- | --- |
| `Robot(double speed_mps)` | 创建 Robot 时需要一个速度参数 |
| `speed_mps` | 本次创建操作收到的临时参数名 |
| `speed_mps_` | 对象内部保存速度的成员名；末尾下划线只是命名习惯 |
| `: speed_mps_{speed_mps}` | 用右边参数初始化左边成员；初始化先于构造函数体执行 |
| `explicit` | 要求明确表达这次构造，减少把 double 意外当 Robot 的情况 |
| `public` | 外部代码可以使用的接口 |
| `private` | 对象内部的数据和实现细节，外部不能直接访问 |

用 `Robot robot{0.8};` 创建对象后，构造函数的参数不需要一直存在，速度已经保存在 robot 自己的成员里。再创建另一个 `Robot other{1.0};`，它会保存自己的 1.0，两个对象互不覆盖。

`double distance(double seconds) const` 末尾的 const 修饰这次成员函数操作：它不通过这个接口修改普通成员。因此 `const Robot robot{0.8};` 也可以调用 distance。参数中的 const 与函数末尾的 const 所处位置不同，不能只看它们长得一样。

## 为什么“自动清理”不用每个类都写 delete

可以把对象看作一只带清单的箱子：Robot 里有一个 double 和一个 vector。销毁 Robot 时，它的成员也依次被销毁；vector 知道如何释放自己管理的存储，所以 Robot 不必重复写这套工作。这就是优先组合现成资源管理类型的理由。

本例的 observations_ 初始为空，只用于说明“成员也有自己的生命周期”，没有在这里实现采集或保存测量值。实际需要数据时再增加接口；不要为了演示 RAII，先堆入没有用途的手动 new/delete。

| 本例的两次创建 | 会经过哪些步骤 | main 接着做什么 |
| --- | --- | --- |
| `Robot{0.8}` | 初始化成员 → 检查通过 → 对象可用 | 调用 distance(5.0)，得到 4 |
| `Robot{-1.0}` | 初始化成员 → 检查失败 → 抛异常 | 跳到 catch，显示 invalid speed |

第二种情况下，完整 Robot 没有构造成功，不能拿来用；已经构造好的成员会清理自身。这也解释了为什么检查失败后那句 `invalid.distance(...)` 不会执行。

### 输入检查的范围要说清楚

`std::isfinite` 表示“不是 NaN，也不是正负无穷大”；`!` 表示取反，`||` 表示任一条件成立。速度为 0、时长为 0 在本例都是合法输入，表示没有走过距离；负输入会被拒绝。

本例用速度乘时间演示成员函数，假设输入在普通教学数值范围。它没有检查乘积是否超出 double 的范围，也没有描述加减速；有限的两个极大数相乘仍可能得到非有限结果。真实距离计算需要补充结果检查和任务所要求的运动模型。

## 完整示例

```cpp title="classes.cpp · 完整示例"
#include <cmath>
#include <iostream>
#include <stdexcept>
#include <vector>

// 把机器人数据与合法操作封装在一起。
class Robot {
public:
    // 构造时直接初始化成员；explicit 避免意外隐式转换。
    // speed_mps 是本次传入的参数，speed_mps_ 是对象一直保存的成员。
    explicit Robot(double speed_mps) : speed_mps_{speed_mps} {
        // 拒绝 NaN/无穷大，也检查物理量不为负。
        if (!std::isfinite(speed_mps) || speed_mps < 0.0) {
            // 输入不符合函数约定，报告原因而不继续计算。
            throw std::invalid_argument("invalid speed");
        }
    }
    // 末尾 const 表示这个操作不修改普通成员。
    double distance(double seconds) const {
        // 拒绝 NaN/无穷大，也检查物理量不为负。
        if (!std::isfinite(seconds) || seconds < 0.0) {
            // 输入不符合函数约定，报告原因而不继续计算。
            throw std::invalid_argument("invalid duration");
        }
        // 米/秒乘秒得到米。
        return speed_mps_ * seconds;
    }
    // 外部代码不能绕过接口随意修改速度。
private:
    double speed_mps_;
    // 容器自动管理内存，不需要自定义 delete 或析构。
    std::vector<double> observations_;
};

// 程序入口；下面按顺序执行示例步骤。
int main() {
    // 创建一个自己的 Robot 对象，保存速度 0.8 米/秒。
    const Robot robot{0.8};
    std::cout << "distance: " << robot.distance(5.0) << " m\n";
    try {
        const Robot invalid{-1.0};
        // 上面的构造已经抛出异常，本行不会执行。
        std::cout << invalid.distance(1.0) << '\n';
    } catch (const std::invalid_argument& error) {
        // 不让失败继续冒出 main，在这里显示构造失败的原因。
        std::cout << error.what() << '\n';
    }
}
```

## 编译与运行

把上面的完整程序保存为 `classes.cpp`，在保存这个文件的目录打开终端。短片段与练习修改不要额外拼在完整程序后面；按正文标明的位置替换或追加。Windows 使用 PowerShell；Linux/macOS 将 `./classes.exe` 换成 `./classes`，并把输出文件名的 `.exe` 去掉。

```powershell
g++ -std=c++17 -Wall -Wextra -Wpedantic classes.cpp -o classes.exe
./classes.exe
```

预期输出：

```text
distance: 4 m
invalid speed
```

## 怎样读这段代码：先创建合法对象，再调用方法

`const Robot robot{0.8}` 分别表示“对象类型是 Robot”“对象名叫 robot”“创建时传入速度 0.8”。Robot 是一个类型，robot 是一份具体对象；可以创建多个 Robot，每份对象保存自己的速度。

| 阶段 | 本例执行的操作 | 接下来为何能继续 |
| --- | --- | --- |
| 创建 robot | 初始化 speed_mps_ 为 0.8，检查有限且非负 | 构造成功，robot 才成为可使用的对象 |
| 调用 distance(5.0) | 参数 seconds 得到 5.0，检查输入后乘以速度 | 返回 4.0，由 cout 输出 distance: 4 m |
| 创建 invalid | 初始化速度为 −1.0，检查失败 | 抛异常，没有得到一个可正常使用的 invalid |
| 处理异常 | catch 取得错误对象，输出 what() | 不再执行 invalid.distance(1.0) |
| main 结束 | 已成功创建的对象按生命周期销毁 | vector 等成员清理各自管理的资源 |

构造函数没有写普通返回类型，名字与类名相同。冒号后面的 `speed_mps_{speed_mps}` 是**用参数初始化成员**：左边带下划线的是对象长期保存的成员，右边是这次构造调用的参数。下划线只是命名习惯，不是语法上自动创建成员的符号。

函数末尾的 const 表达“这个成员操作不通过普通成员修改对象”。所以对 const robot 也能调用 distance。参数 seconds 每次调用都重新取得本次输入；speed_mps_ 则一直保存在 robot 内。`distance(2.0)` 会用同一速度算出 1.6，而不是沿用上一次调用的 5 秒。

RAII 的关键是资源跟着管理对象的生命周期。本例没有手写 delete：observations_ 是 vector，vector 自己管理其内存。它是教学用的空成员，并没有读取传感器。创建失败时，已构造的成员仍会清理，但未完成构造的整个 Robot 不会执行自身析构函数。

### private 为何有用？

如果外部代码能直接把速度成员改成 −1，构造时的检查就容易被绕过。private 把修改入口收进类的接口中；之后若添加设置速度的方法，也应在那个入口重新检查。合法状态靠所有修改入口维持，不能只给一个构造函数加检查就随意开放别的写入口。

## 常见错误

- 正常退出作用域和异常栈展开会清理对象；强制结束进程、断电不保证析构。
- 析构函数尽量不要抛异常，尤其在处理另一个异常时。
- 需要通过基类指针删除派生类时，基类必须具有合适的虚析构函数；本例没有继承需求。

## 动手练习

<div class="practice-card" markdown="1">

<p class="practice-kicker">接着正文做一个小改动</p>

<p class="practice-title">在对象出生时检查电量</p>

类已经拒绝非法速度。把同样的接口约定扩展到电量，练习“数据和检查放在一起”。

**从哪里开始**：修改 Robot 的构造函数，并在 private 部分增加 battery_percent_ 成员。

**按这几步做**：

1. 新增电量参数，约定单位是百分比。
2. 在成员初始化列表里保存它。
3. 拒绝非有限数、小于 0 和大于 100 的输入。

??? tip "需要一点提示？"

    需要同时更新参数列表、初始化列表和私有成员声明；不要只改检查条件。

??? example "查看参考修改与解释"

    合法电量范围包含 0 和 100。下面的构造函数替换原构造函数，私有成员声明加在现有成员旁边。之后用 Robot{0.8, 80.0} 创建对象。

    **放在哪里**：这是类成员的修改片段；main 中所有 Robot 构造调用都要补上电量参数。

    ```cpp
    explicit Robot(double speed_mps, double battery_percent)
        : speed_mps_{speed_mps}, battery_percent_{battery_percent} {
        if (!std::isfinite(speed_mps) || speed_mps < 0.0) {
            throw std::invalid_argument("invalid speed");
        }
        if (!std::isfinite(battery_percent)
            || battery_percent < 0.0 || battery_percent > 100.0) {
            throw std::invalid_argument("invalid battery");
        }
    }

    // 这一行放到 private 区域，不放在构造函数内部。
    double battery_percent_;
    ```

    **核对这段修改的结果**：

    | 电量输入 | 应有结果 |
    | --- | --- |
    | 0、80、100 | 对象可以创建 |
    | −1、101、NaN | 拒绝创建，报告 invalid battery |

</div>


## 延伸阅读

[规范或官方指南](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)。标准草案会继续更新，查阅时注意条款可能包含晚于本章示例的功能。


---

[返回学习路线](index.md) · [上一章：03 · 函数、引用与 const](functions.md) · [下一章：05 · 容器与标准算法 →](containers.md)
