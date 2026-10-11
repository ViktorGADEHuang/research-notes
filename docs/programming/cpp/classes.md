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

## 完整示例

```cpp
#include <cmath>
#include <iostream>
#include <stdexcept>
#include <vector>

// 把机器人数据与合法操作封装在一起。
class Robot {
public:
    // 构造时直接初始化成员；explicit 避免意外隐式转换。
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
    std::vector<double> observations_; // Automatically releases its memory.
};

// 程序入口；下面按顺序执行示例步骤。
int main() {
    const Robot robot{0.8};
    std::cout << "distance: " << robot.distance(5.0) << " m\n";
    try {
        const Robot invalid{-1.0};
        std::cout << invalid.distance(1.0) << '\n';
    // 处理对应类型的异常；通过 const 引用避免复制异常对象。
    } catch (const std::invalid_argument& error) {
        std::cout << error.what() << '\n';
    }
}
```

## 编译与运行

在示例目录执行。Windows 使用 PowerShell；Linux/macOS 将 `./classes.exe` 换成 `./classes`，并把输出文件名的 `.exe` 去掉。

```powershell
g++ -std=c++17 -Wall -Wextra -Wpedantic classes.cpp -o classes.exe
./classes.exe
```

预期输出：

```text
distance: 4 m
invalid speed
```

## 怎样读这段代码

成员初始化列表 `: speed_mps_{speed_mps}` 直接初始化成员；`explicit` 阻止一些意外的隐式转换。函数末尾的 `const` 表示它不通过普通成员修改该对象，因此能在 `const Robot` 上调用。

速度乘时间得到距离，单位分别是米/秒、秒、米。`observations_` 是教学用的资源成员：即便类没有自定义析构函数，它也会自动销毁。

如果构造函数抛异常，已构造完成的成员会清理；这个未构造成功的完整对象不会执行自身析构函数。

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
