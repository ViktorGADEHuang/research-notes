# 08 · Lambda 与回调

**示例标准：C++17**

Lambda 是写在使用位置附近的函数。像“把大于阈值的距离留下来”这种短规则，用 Lambda 就不用跳到另一个文件找函数定义。


!!! tip "读完这页，你应该能做到"

    比较按值捕获和按引用捕获，并找出生命周期要求。

    **先会这些就够了**：函数、引用。


## 看图梳理

![Lambda 如何使用外部变量](../../assets/learning/cpp-lambdas.svg){ .learning-figure }

[打开大图](../../assets/learning/cpp-lambdas.svg)

**按值捕获**：[threshold]，保存创建时的副本；**按引用捕获**：[＆threshold]，使用外部当前值；**生命周期**：稍后调用的回调，引用对象不能先销毁。


## 为什么短规则常常写在使用位置

给 count_if 一条“距离超过阈值”的规则，没必要为了几字逻辑到远处找定义。Lambda 会创建一个可调用对象，你可以把它交给算法，也可以保存后再调用。

关键是规则要怎样拿到外面的 threshold。创建时阈值为 2，随后外面改为 4，再检查距离 3：

| 捕获方式 | 调用时读到什么 | 判断结果 |
| --- | --- | --- |
| `[threshold]` | 创建时保存的副本 2 | 3 > 2，true |
| `[&threshold]` | 外面这个变量现在的值 4 | 3 > 4，false |

捕获列表是方括号，调用参数是圆括号，函数体是花括号，三者作用不同。按值捕获不是每次调用都重新复制外部值，按引用捕获也不是自动保证外部对象永远存在。

下面立即在 main 内调用，threshold 还活着。把回调交给异步任务时，要另外检查它将来调用时变量是否已销毁；先掌握这个区别，再学复杂回调框架。


## 一行语法拆开看

`[threshold](double d) { return d > threshold; }`

1. `[threshold]`：捕获外部变量，这里保存阈值的副本。
2. `(double d)`：输入参数。
3. `{ ... }`：函数体。

`[&threshold]` 按引用捕获，访问原变量；`[]` 不捕获外部局部变量。回调是“交给别人、稍后由别人调用的函数”。Lambda 是写回调的一种方式。

`auto` 可以保存具体 Lambda 类型。`std::function` 可以保存符合签名的不同可调用对象，但有类型擦除开销，有些情况还会动态分配，别无条件套一层。

## 定义一条规则，与执行一次规则，是两个动作

以下片段放在 main 内，已有 `<iostream>` 即可。先故意不用任何捕获，认识最短的 Lambda：

```cpp
const auto is_far = [](double distance_m) {
    return distance_m > 2.0; // 这里描述规则；定义时还没有具体距离。
};                          // Lambda 表达式赋给变量，整条声明需要分号。
std::cout << std::boolalpha;
std::cout << is_far(1.0) << '\n'; // 这才调用，输出 false。
std::cout << is_far(3.0) << '\n'; // 再调用一次，输出 true。
```

这里 auto 推导的是编译器生成的可调用对象类型，并不是 bool。**调用它之后返回的结果**才是 bool。可以把 is_far 理解为存了一张处理规则，每次递给它一个距离，它回给你“是”或“否”。

## 捕获变量与传入参数，为什么需要两处括号

把固定的 2.0 改成外部 threshold 后，这条规则要同时认识两件东西：长期记住或借用的阈值、每次调用收到的新距离。

| 部分 | 什么时候确定 | 可以想成什么 |
| --- | --- | --- |
| `[threshold]` | 创建 Lambda 的这一刻 | 把阈值抄在规则纸上 |
| `[&threshold]` | 创建时建立借用，调用时读当前值 | 记住去哪里看原阈值 |
| `(double d)` | 每次调用时 | 这次要检查的那个距离 |
| `return d > threshold` | 每次调用执行时 | 按规则算出这一次的真假 |

原例里 by_value 创建时把 2.0 留在内部副本里；后来外部 threshold 改为 4.0，只影响原变量。by_reference 看同一个原变量，因此会看到 4.0。按值与按引用都没有“自动比较哪个值更新”这种机制。

## count_if 是怎么调用你的规则的

`std::count_if(..., by_reference)` 的第三个参数是**规则本身**，没有写 `by_reference(...)`。算法会取出列表中的元素，再代你调用。下面是理解用的等价计数过程，放在原例 distances 声明之后即可，结果也是 1：

```cpp
int count{0};
for (double distance_m : distances) {
    if (by_reference(distance_m)) { // 算法内部需要的正是这种判断。
        ++count;
    }
}
std::cout << count << '\n';
```

这里“交给别人调用”就是回调，并不意味着必须等待很久、必须开线程或必须联网。count_if 会在这次调用期间完成检查。事件系统或线程以后才调用的回调，则需要另外考虑被捕获对象的生命周期。

初学优先写清具体捕获名。`[=]`、`[&]` 这样的默认捕获更省字符，却容易把不该延长借用的局部变量带进回调。是否按值保存、是否借用，先根据数据是否需要更新、调用发生在何时来决定。

## 完整示例

```cpp title="lambdas.cpp · 完整示例"
#include <algorithm>
#include <iostream>
#include <vector>

// 程序入口；下面按顺序执行示例步骤。
int main() {
    double threshold{2.0};
    // 保存此刻阈值的副本，之后外部修改不会同步进去。
    const auto by_value = [threshold](double d) { return d > threshold; };
    // 借用外部阈值，使用时必须确保原变量还活着。
    const auto by_reference = [&threshold](double d) { return d > threshold; };
    // 修改原变量，用来展示两种捕获方式的差别。
    threshold = 4.0;
    // boolalpha 让判断结果显示为 true / false，便于对照纸上推演。
    std::cout << std::boolalpha;
    std::cout << "value capture: " << by_value(3.0) << '\n';
    std::cout << "reference capture: " << by_reference(3.0) << '\n';
    const std::vector<double> distances{1.0, 3.0, 5.0};
    // count_if 遍历距离，每次调用 by_reference(当前距离)。
    // 只有 5.0 大于现在的 4.0，所以最终计数是 1。
    std::cout << "above current threshold: "
              << std::count_if(distances.begin(), distances.end(), by_reference)
              << '\n';
}
```

## 编译与运行

把上面的完整程序保存为 `lambdas.cpp`，在保存这个文件的目录打开终端。短片段与练习修改不要额外拼在完整程序后面；按正文标明的位置替换或追加。Windows 使用 PowerShell；Linux/macOS 将 `./lambdas.exe` 换成 `./lambdas`，并把输出文件名的 `.exe` 去掉。

```powershell
g++ -std=c++17 -Wall -Wextra -Wpedantic lambdas.cpp -o lambdas.exe
./lambdas.exe
```

预期输出：

```text
value capture: true
reference capture: false
above current threshold: 1
```

## 怎样读这段代码：保存规则时与调用规则时分开

threshold 初始为 2.0，两份 Lambda 都在此时创建。by_value 保存一份阈值副本，by_reference 保存对外部变量的访问关系；之后把外部 threshold 改为 4.0。

| 发生的操作 | by_value 看到的阈值 | by_reference 看到的阈值 |
| --- | --- | --- |
| 创建两份规则时 | 保存 2.0 的副本 | 关联到外面的 threshold |
| 外面赋值为 4.0 | 仍是 2.0 | 调用时读取外面的 4.0 |
| 用距离 3.0 调用 | 3 > 2，返回 true | 3 > 4，返回 false |

这里有两种输入来源：圆括号里的 double d 是**每次调用时提供的距离**；方括号里捕获的 threshold 是**创建规则时决定怎样取得的背景数据**。两者不是同一个参数列表。

接着 count_if 读取 {1, 3, 5}，依次调用 by_reference。阈值此时仍为 4，所以三次返回 false、false、true，统计为 1。将函数传给算法时写 by_reference，是交出一个可调用对象；写 by_reference(3.0)，则先执行它，交出的是一次判断的真假结果，类型与用途不同。

### 按引用捕获为什么要看调用时机？

本例的调用都在 main 内，threshold 尚未结束生命周期，因此引用有效。若把规则存到更长寿的对象中，等原变量已销毁再调用，就不能沿旧引用访问。捕获 & 很方便，但必须同时知道被捕获对象的负责人以及规则何时执行。

Lambda 并不因为没有名字就立即执行，也不自动启动线程。它是一个可以保存、传递、调用的短函数对象；是否调用、调用几次、在哪个线程调用，由使用它的代码决定。

## 常见错误

- 返回一个捕获局部变量引用的 Lambda 后，局部变量销毁，再调用会访问悬空引用。
- 异步任务中捕获引用要特别检查生命周期；捕获 `this` 也没有自动延长对象生命周期。
- 大对象按值捕获可能复制很多数据。`[data = std::move(data)]` 可转移到闭包里，但调用者应理解所有权已经改变。

## 动手练习

<div class="practice-card" markdown="1">

<p class="practice-kicker">接着正文做一个小改动</p>

<p class="practice-title">改了阈值，谁会跟着变化</p>

你已经看过按值与按引用捕获的差别。这次用更小的阈值判断同一距离，确认各自保存的是什么。

**从哪里开始**：沿用 lambdas.cpp 中两个 Lambda 的定义，把创建之后的阈值赋值与输出替换掉。

**按这几步做**：

1. 创建 Lambda 时仍让 threshold 为 2.0。
2. 随后将外部 threshold 改为 0.5。
3. 两个 Lambda 都检查距离 1.0，先预测再看答案。

??? tip "需要一点提示？"

    按值捕获保留创建时的 2.0；按引用捕获读取现在的 0.5。

??? example "查看参考修改与解释"

    1.0 不大于 2.0，但大于 0.5，所以按值捕获为 false，按引用捕获为 true。

    **放在哪里**：保留 main 开头的 threshold 和两个 Lambda；替换后面的赋值与演示输出。

    ```cpp
    threshold = 0.5;
    std::cout << std::boolalpha;
    std::cout << "value capture: " << by_value(1.0) << '\n';
    std::cout << "reference capture: " << by_reference(1.0) << '\n';
    ```

    **核对这段修改的结果**：

    ```text
    value capture: false
    reference capture: true
    ```

</div>


## 延伸阅读

[规范或官方指南](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)。标准草案会继续更新，查阅时注意条款可能包含晚于本章示例的功能。


---

[返回学习路线](index.md) · [上一章：07 · 模板与泛型编程](templates.md) · [下一章：09 · 移动语义 →](move.md)
