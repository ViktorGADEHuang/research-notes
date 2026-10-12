# 09 · 移动语义

**示例标准：C++17**

复制像把一份资料重新抄一遍；移动像允许另一对象接手原来的资料。移动可能减少分配和复制，但只有类型提供合适的移动操作时才能得到这个效果。


!!! tip "读完这页，你应该能做到"

    理解 std::move 只是允许移动，不能假定所有源对象都为空。

    **先会这些就够了**：容器、所有权。


## 看图梳理

![复制与移动的区别](../../assets/learning/cpp-move.svg){ .learning-figure }

[打开大图](../../assets/learning/cpp-move.svg)

**复制**：创建独立副本，两个对象各自管理数据；**允许移动**：std::move 是转换，构造或赋值执行转移；**移动之后**：源对象仍需按约定用，不要假定所有类型为空。


## 复制与移动，分别想解决什么问题

复制是“再做一份独立数据”：改 copy 不影响原列表。移动是“允许接收方接手原对象的资源”：对于下面普通 vector 的移动构造，可以转交底层存储，避免逐个复制元素。

`std::move` 本身只是改变表达式的类别，像告诉接收方“这份资源允许接手”。真正的移动发生在接收方的构造或赋值中；如果类型没有合适的移动操作，仍可能复制。

| 本例行为 | 要核对的结果 |
| --- | --- |
| 复制列表后把副本首项改为 9 | 原首项仍为 1 |
| 把原列表移动构造为 moved | moved 有原来的三个元素 |
| 对源列表 clear，再加入 7 | 源对象可重新使用 |
| 移动 unique_ptr | 新拥有者拿到 42，旧拥有者为空 |

不要把所有源对象都想成移动后必定空：不同类型的保证不同。下面刻意先 clear 再复用源 vector，避免依赖未指定状态；unique_ptr 则明确保证移动后源指针为空。


## std::move 到底做了什么

`std::move(x)` 本身不搬数据，它把表达式转换成允许被移动的形式（通常称为右值引用形式）。之后的构造或赋值才决定执行移动还是复制。

`T&&` 表示右值引用；在模板参数推导的特定情形下，也可以是转发引用。初学先掌握“移动后不要假定原数据还在”，再学 `std::forward` 的完美转发。

对标准库对象，移动后通常处于**有效但未指定的状态**，除非相应类型另有保证。`unique_ptr` 有明确的空指针保证；不能把它推广成“所有容器移动后一定为空”。

## 用同一份列表追踪：到底哪个对象发生了变化

后面完整程序按下表顺序执行。表中的“未作内容假设”不是对象坏了，而是教程选择不依赖它移动后的具体内容：

| 刚执行完的语句 | original | copy | moved |
| --- | --- | --- | --- |
| 创建 original | 1、2、3 | 尚未创建 | 尚未创建 |
| `auto copy = original` | 1、2、3 | 1、2、3 | 尚未创建 |
| `copy[0] = 9` | 1、2、3 | 9、2、3 | 尚未创建 |
| `auto moved = std::move(original)` | 未作内容假设 | 9、2、3 | 1、2、3 |
| `original.clear()` | 空 | 9、2、3 | 1、2、3 |
| `original.push_back(7)` | 7 | 9、2、3 | 1、2、3 |

`auto copy = original` 中虽然出现等号，但 copy 正在被创建，所以这里调用的是**复制构造**；若 copy 早已存在，再写 `copy = original`，才是复制赋值。移动也有相同区别：创建新对象与覆盖已有对象走不同操作。

## “有效但未指定”应该怎样使用

有效意味着它仍然是一个可以按类型规则操作、最终可以销毁的对象；未指定意味着你不要依赖某一种内容。对这里的标准容器，可以调用 clear，把它置空，再加入新数据。也可以查询 empty，但不能无条件用 `[0]` 假设还有第一个元素。

如果想读移动后源容器的第一项，至少先确认它确实非空；不过当前任务本来就是把旧数据交给 moved，直接从 moved 读取更清楚。对自定义类型，要看该类型自己承诺的移动后状态，不能机械套用某个容器的结论。

std::move 写上去也不代表程序完成了某种“通用搬家”。它是一个转换，接收方是否有合适的移动构造/赋值、是否允许从这个源类型移动，才决定后续动作。标准库对移动后状态的总体规则可查 [标准库类型要求](https://eel.is/c++draft/lib.types.movedfrom)。

### 不要把 const 与“允许拿走”放在一起猜

常见移动操作需要改动源对象，所以通常接收非 const 源。`std::move` 不会去掉 const；对 const vector 使用它，通常只能匹配复制构造。指针拥有关系、引用与 const 都是在表达约定，不能为了追求“看起来更快”而无差别添加 std::move。

这章先掌握读现成类型的移动。手写移动构造涉及异常保证、资源状态等更多规则；用 vector、string、unique_ptr 组合类时，通常可以先让成员完成这些工作。

## 完整示例

```cpp title="move.cpp · 完整示例"
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
    std::cout << "original first: " << original[0] << '\n';
    // 对照输出：副本变为 9，上一行输出的原列表仍为 1。
    std::cout << "copy first: " << copy[0] << '\n';
    // std::move 允许移动构造，实际转移由 vector 完成。
    auto moved = std::move(original);
    std::cout << "moved size: " << moved.size() << '\n';
    // 不依赖移动后内容；先清空，再把源对象用于新数据。
    original.clear();
    // 移动后的 vector 仍有效，可重新使用。
    original.push_back(7);
    std::cout << "reused original: " << original[0] << '\n';
    // 新建一个值为 42 的整数，交给唯一拥有者管理。
    auto owner = std::make_unique<int>(42);
    // unique_ptr 禁止复制，但可移动转交资源。
    auto recipient = std::move(owner);
    std::cout << "recipient: " << *recipient << '\n';
}
```

## 编译与运行

把上面的完整程序保存为 `move.cpp`，在保存这个文件的目录打开终端。短片段与练习修改不要额外拼在完整程序后面；按正文标明的位置替换或追加。Windows 使用 PowerShell；Linux/macOS 将 `./move.exe` 换成 `./move`，并把输出文件名的 `.exe` 去掉。

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

## 怎样读这段代码：对象还在，资源责任发生转移

先分清三个 vector 对象：original、copy、moved。复制以后，copy 有自己独立管理的元素；移动以后，moved 获得原来的三个元素，但 original 这个对象仍然存在。

| 步骤 | original | copy | moved |
| --- | --- | --- | --- |
| 初始 | {1, 2, 3} | 尚未创建 | 尚未创建 |
| auto copy = original | {1, 2, 3} | 独立的 {1, 2, 3} | 尚未创建 |
| copy[0] = 9 | {1, 2, 3} | {9, 2, 3} | 尚未创建 |
| auto moved = std::move(original) | 有效，内容按允许的状态处理 | {9, 2, 3} | 有原来的三个元素 |
| original.clear(); push_back(7) | {7} | {9, 2, 3} | 继续保留自己的三个元素 |

std::move 是一种转换，表示允许后续操作把这个对象当作可移动的来源。**实际怎样移动由接收方的构造或赋值操作完成。** 只调用 std::move 而没有接收操作，不会凭空生成另一个容器。

移动后本例不读取 original[0]，因为还不知道里面有没有元素；先 clear，再 push_back，才有明确可读取的第 0 项。这比猜测“每种对象移动后都一定为空”更稳妥。对于 unique_ptr，移动后源指针为空则是它明确提供的保证。

最后 owner 管理整数 42，recipient 通过移动接手，所以 *recipient 得到 42。owner 的对象还在，却已经不拥有那个整数；这里不再通过 owner 解引用。对象是否存在、是否还持有资源、当前内容是否可依赖，应分别判断。

### 为什么不是所有情况都值得移动？

移动的用途是在合适接口下转交资源，而不是给每个变量都加 std::move。像 int 这样很小的值，本来复制就简单；const 对象也常因无法交出可修改的来源而选择复制。先画清数据需要几份、下一步谁还需要用原对象，再决定复制、借用还是转交。

## 常见错误

- 不要处处加 `std::move`；在返回局部变量时通常直接 `return result;`，强行 move 可能妨碍返回值优化。
- 手写拥有资源的类时，复制、移动、析构要协调；尽可能采用 Rule of Zero。
- 移动不保证总比复制快，小的基本类型移动没有特别的性能优势。

## 动手练习

<div class="practice-card" markdown="1">

<p class="practice-kicker">接着正文做一个小改动</p>

<p class="practice-title">从一个新的资源开始练习移动</p>

原例已经把 owner 的资源转给 recipient，再移动旧 owner 只会转交空指针。这次重新创建资源，避免混淆练习起点。

**从哪里开始**：在 move.cpp 的 main 中，替换原来的 unique_ptr 演示部分；前面的 vector 演示可保留。

**按这几步做**：

1. 先创建值为 42 的新 unique_ptr。
2. 只在纸上判断直接复制为什么被拒绝，不把错误语句加入正常示例。
3. 用 std::move 转交给 second，再检查原指针和新资源。

??? tip "需要一点提示？"

    auto second = owner; 需要复制 unique_ptr，它没有复制构造；移动才允许转移所有权。

??? example "查看参考修改与解释"

    移动后 owner 为空，second 持有 42。强调“允许移动”仍由类型的移动操作实现，不是 std::move 自己搬运资源。

    **放在哪里**：替换原有 owner / recipient 演示，避免在同一作用域重复声明 owner。

    ```cpp
    auto owner = std::make_unique<int>(42);
    // 不写 auto second = owner;，unique_ptr 不允许复制。
    auto second = std::move(owner);
    std::cout << std::boolalpha << "old owner empty: " << !owner << '\n';
    std::cout << "new value: " << *second << '\n';
    ```

    **核对这段修改的结果**：

    ```text
    old owner empty: true
    new value: 42
    ```

</div>


## 延伸阅读

[规范或官方指南](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)。标准草案会继续更新，查阅时注意条款可能包含晚于本章示例的功能。


---

[返回学习路线](index.md) · [上一章：08 · Lambda 与回调](lambdas.md) · [下一章：10 · C++17 常用工具 →](cpp17.md)
