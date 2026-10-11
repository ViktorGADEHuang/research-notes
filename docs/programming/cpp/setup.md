# 01 · 环境与第一个程序

写 C++ 需要两类工具：编辑器负责写代码，编译器把代码变成可执行程序。VS Code 是编辑器，安装 C++ 扩展不等于已经安装编译器。


!!! tip "读完这页，你应该能做到"

    分清编辑器和编译器，知道编译失败后不能用旧程序验证新代码。

    **先会这些就够了**：无需 C++ 基础。


## 看图梳理

![从代码到程序](../../assets/learning/cpp-setup.svg){ .learning-figure }

[打开大图](../../assets/learning/cpp-setup.svg)

**编辑源文件**：hello.cpp，检查括号与分号；**编译与链接**：选择 C++ 标准，把定义组成程序；**启动程序**：执行生成的文件，核对输出与错误。


## 选择一条安装路线

| 平台 | 一条常见路线 | 检查 |
| --- | --- | --- |
| Windows | [MSYS2 官方安装](https://www.msys2.org/)后使用 UCRT64 环境 | UCRT64 终端执行 `g++ --version` |
| Windows | [Visual Studio C++ 工具](https://learn.microsoft.com/en-us/cpp/build/vscpp-step-0-installation) | 开发者命令提示符执行 `cl` |
| Linux | 使用发行版包管理器安装 GCC/G++ | `g++ --version` |
| macOS | 安装 Xcode 命令行开发工具，使用 Apple Clang | `clang++ --version` |

本教程命令主要用 G++。如果用 MSYS2，在 **UCRT64** 终端安装 `mingw-w64-ucrt-x86_64-gcc`；不要把 MSYS、MINGW64、UCRT64 的不同工具链混在一起。照 [MSYS2 入门文档](https://www.msys2.org/docs/environments/)选对应终端。

PowerShell 找不到 g++ 时，把实际安装目录的 `ucrt64/bin` 加入 PATH 并重新打开终端，或直接使用编译器完整路径。编译与运行应能找到同一工具链的 DLL，不要从其他来源随意复制 DLL 来凑。

## 第一个程序

新建 `hello.cpp`：

```cpp
#include <iostream>

int main() {
    // cout 输出文字，\n 表示换行。
    std::cout << "Hello, C++!\n";
    // 返回 0 告诉操作系统：程序正常结束。
    return 0;
}
```

`#include` 让程序看得到输出工具的声明；`main` 是入口；`std::cout` 输出文本；`return 0` 表示正常结束。main 走到末尾也会隐式返回 0。

Windows PowerShell：

```powershell
g++ -std=c++17 -Wall -Wextra -Wpedantic hello.cpp -o hello.exe
./hello.exe
```

Linux/macOS：

```bash
g++ -std=c++17 -Wall -Wextra -Wpedantic hello.cpp -o hello
./hello
```

macOS 可把 g++ 换成 clang++。输出应是 `Hello, C++!`。`-std=c++17` 选择标准，`-Wall -Wextra -Wpedantic` 开启常见警告，`-o` 指定输出文件。选项含义见 [GCC 官方文档](https://gcc.gnu.org/onlinedocs/gcc/C_002b_002b-Dialect-Options.html)。

MSVC 用户请在开发者终端执行：

```text
cl /std:c++17 /EHsc /W4 /utf-8 hello.cpp /Fe:hello.exe
hello.exe
```

C++20 示例可改为 `/std:c++20`。C++23 开关与功能支持请按所装 MSVC 版本查 [官方 /std 文档](https://learn.microsoft.com/en-us/cpp/build/reference/std-specify-language-standard-version)，不要把 G++ 的参数直接传给 cl。

## 出错时先分清阶段

| 阶段 | 常见现象 | 先检查 |
| --- | --- | --- |
| 找工具 | g++ 不是可识别命令 | 是否装编译器、PATH 是否正确 |
| 编译 | expected 不存在、语法错误 | 标准开关、头文件、库版本、第一条错误 |
| 链接 | undefined reference | 是否漏编源文件或库 |
| 运行 | 找不到 DLL、输出异常 | 运行环境、输入、边界和生命周期 |

编译失败后不要直接运行上次留下的 exe，旧程序会造成“修改没有生效”的错觉。

## 动手练习

<div class="practice-card" markdown="1">

<p class="practice-kicker">接着正文做一个小改动</p>

<p class="practice-title">让第一段程序说出你的实验信息</p>

你已经认识了 main 和 cout。这次只改输出文字，练习“编辑源码 → 重新编译 → 查看新结果”。

**从哪里开始**：在 hello.cpp 的 main 里，替换原来的 Hello 输出语句，保留函数括号和 return。

**按这几步做**：

1. 让第一行输出实验名称，第二行输出研究方向。
2. 先检查每条语句的分号，再重新编译。
3. 可选：临时漏掉一个分号，观察第一条报错后恢复。

??? tip "需要一点提示？"

    字符串里的 \n 表示换行；编译失败时不要运行上次留下的 exe。

??? example "查看参考修改与解释"

    先让输出正确，再用一个小错误认识编译提示。错误位置有时落在下一行，因此也要检查上一行。

    **放在哪里**：只替换 main 内的输出语句，不另写一个 main。

    ```cpp
    // 两次输出分别占一行，放在 main 内。
    std::cout << "Viktor research notes\n";
    std::cout << "Herding robotics\n";
    ```

    **核对这段修改的结果**：

    ```text
    Viktor research notes
    Herding robotics
    ```

</div>


[继续：变量、判断与循环 →](basics.md)


---

[返回学习路线](index.md) · [下一章：02 · 变量、判断与循环 →](basics.md)
