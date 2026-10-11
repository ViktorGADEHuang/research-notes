# 04 · 类与 RAII

**示例标准：C++17** · [下载完整代码](examples/classes.cpp)

类把相关数据和操作放到一起。RAII 的直觉是：让对象替你保管资源，对象离开作用域时自动归还。资源可以是内存、文件、锁，也可以是设备连接。


!!! tip "读完这页，你应该能做到"

    解释构造检查和成员自动清理为什么能减少资源错误。

    **先会这些就够了**：函数、const。


## 看图梳理

![类怎样维持合法状态](../../assets/learning/cpp-classes.svg){ .learning-figure }

[打开大图](../../assets/learning/cpp-classes.svg)

**构造时**：初始化成员，拒绝非法速度；**使用时**：公开受控接口，只读操作加 const；**销毁时**：成员自动析构，资源跟随生命周期。


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

增加电量 `battery_percent`，限制在 0～100，构造时拒绝越界输入。

??? tip "展开参考答案"

    添加私有 `double battery_percent_`，在初始化列表赋值，再用 `!std::isfinite(battery_percent) || battery_percent < 0 || battery_percent > 100` 检查。不能只检查小于 0，否则 NaN 可能漏过。

## 延伸阅读

[规范或官方指南](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)。标准草案会继续更新，查阅时注意条款可能包含晚于本章示例的功能。


---

[返回学习路线](index.md) · [上一章：03 · 函数、引用与 const](functions.md) · [下一章：05 · 容器与标准算法 →](containers.md)
