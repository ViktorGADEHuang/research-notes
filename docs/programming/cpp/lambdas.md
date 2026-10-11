# 08 · Lambda 与回调

**示例标准：C++17** · [下载完整代码](examples/lambdas.cpp)

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

## 完整示例

```cpp
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
    std::cout << std::boolalpha;
    std::cout << "value capture: " << by_value(3.0) << '\n';
    std::cout << "reference capture: " << by_reference(3.0) << '\n';
    const std::vector<double> distances{1.0, 3.0, 5.0};
    std::cout << "above current threshold: "
              // 算法会调用传入的 Lambda 检查每个元素。
              << std::count_if(distances.begin(), distances.end(), by_reference)
              << '\n';
}
```

## 编译与运行

在示例目录执行。Windows 使用 PowerShell；Linux/macOS 将 `./lambdas.exe` 换成 `./lambdas`，并把输出文件名的 `.exe` 去掉。

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

## 怎样读这段代码

按值捕获保存创建 Lambda 时的 2.0；以后外部变量改成 4.0，并不会同步更新那份副本。按引用捕获读到当前 4.0。

`count_if` 调用回调检查三个距离，只有 5.0 大于当前阈值，所以结果是 1。两个 Lambda 都在 `threshold` 仍存在的 `main` 内调用，引用没有悬空。

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
