# 09 · 移动语义

**示例标准：C++17** · [下载完整代码](examples/move.cpp)

复制像把一份资料重新抄一遍；移动像允许另一对象接手原来的资料。移动可能减少分配和复制，但只有类型提供合适的移动操作时才能得到这个效果。


## 看图梳理

![复制与移动的区别](../../assets/learning/cpp-move.svg){ .learning-figure }

[打开大图](../../assets/learning/cpp-move.svg)

**复制**：创建独立副本，两个对象各自管理数据；**允许移动**：std::move 是转换，构造或赋值执行转移；**移动之后**：源对象仍需按约定用，不要假定所有类型为空。


## std::move 到底做了什么

`std::move(x)` 本身不搬数据，它把表达式转换成允许被移动的形式（通常称为右值引用形式）。之后的构造或赋值才决定执行移动还是复制。

`T&&` 表示右值引用；在模板参数推导的特定情形下，也可以是转发引用。初学先掌握“移动后不要假定原数据还在”，再学 `std::forward` 的完美转发。

对标准库对象，移动后通常处于**有效但未指定的状态**，除非相应类型另有保证。`unique_ptr` 有明确的空指针保证；不能把它推广成“所有容器移动后一定为空”。

## 完整示例

```cpp
#include <iostream>
#include <memory>
#include <utility>
#include <vector>

// 程序入口；下面按顺序执行示例步骤。
int main() {
    std::vector<int> original{1, 2, 3};
    // 复制出独立容器，修改副本不影响原列表。
    auto copy = original;
    // 只修改副本的第一个元素。
    copy[0] = 9;
    // 把结果输出到终端，便于与正文中的示例结果对照。
    std::cout << "original first: " << original[0] << '\n';
    // 只修改副本的第一个元素。
    std::cout << "copy first: " << copy[0] << '\n';
    // std::move 允许移动构造，实际转移由 vector 完成。
    auto moved = std::move(original);
    // 把结果输出到终端，便于与正文中的示例结果对照。
    std::cout << "moved size: " << moved.size() << '\n';
    // 不依赖移动后内容；先清空，再把源对象用于新数据。
    original.clear(); // Valid regardless of its unspecified contents.
    // 移动后的 vector 仍有效，可重新使用。
    original.push_back(7);
    // 把结果输出到终端，便于与正文中的示例结果对照。
    std::cout << "reused original: " << original[0] << '\n';
    auto owner = std::make_unique<int>(42);
    // unique_ptr 禁止复制，但可移动转交资源。
    auto recipient = std::move(owner);
    // 把结果输出到终端，便于与正文中的示例结果对照。
    std::cout << "recipient: " << *recipient << '\n';
}
```

## 编译与运行

在示例目录执行。Windows 使用 PowerShell；Linux/macOS 将 `./move.exe` 换成 `./move`，并把输出文件名的 `.exe` 去掉。

```powershell
g++ -std=c++17 -Wall -Wextra -Wpedantic move.cpp -o move.exe
./move.exe
```

预期输出：

```text
original first: 1
copy first: 9
moved size: 3
reused original: 7
recipient: 42
```

## 怎样读这段代码

复制后的列表与原列表独立，修改 `copy[0]` 不改变原值。普通 `vector` 的移动构造可接手底层存储，目标有原来的三个元素。

我们不输出并依赖源列表的大小，而是先 `clear` 再重新放入 7，使用它处于有效状态的保证。`unique_ptr` 不能复制，因为不能出现两个唯一拥有者，但可以移动。

`std::move` 一个 `const` 对象经常会选择复制，因为常见移动构造需要修改源对象，接收 `T&&` 而不是 `const T&&`。

## 常见错误

- 不要处处加 `std::move`；在返回局部变量时通常直接 `return result;`，强行 move 可能妨碍返回值优化。
- 手写拥有资源的类时，复制、移动、析构要协调；尽可能采用 Rule of Zero。
- 移动不保证总比复制快，小的基本类型移动没有特别的性能优势。

## 动手练习

尝试写 `auto second = owner;`，为什么不能编译？该怎样转移它？

??? tip "展开参考答案"

    `unique_ptr` 禁用了复制。要转移时写 `auto second = std::move(owner);`，转移前必须确认 `owner` 当前有你要的资源；本例已转给 recipient，再次移动只会得到空指针。

## 延伸阅读

[规范或官方指南](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)。标准草案会继续更新，查阅时注意条款可能包含晚于本章示例的功能。


---

[返回学习路线](index.md) · [上一章：08 · Lambda 与回调](lambdas.md) · [下一章：10 · C++17 常用工具 →](cpp17.md)
