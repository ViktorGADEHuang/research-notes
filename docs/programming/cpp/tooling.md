# 14 · CMake、警告与调试

只有一个文件时，一条编译命令就够。文件变多后，CMake 记录“哪些源文件组成哪个程序、需要什么标准”，避免每次手写越来越长的命令。CMake 自己不是 C++ 编译器。


!!! tip "读完这页，你应该能做到"

    分清配置、编译、链接、运行的错误，并读懂构建目标。

    **先会这些就够了**：独立 cpp 示例。


## 看图梳理

![CMake 构建与排错](../../assets/learning/cpp-tooling.svg){ .learning-figure }

[打开大图](../../assets/learning/cpp-tooling.svg)

**声明目标**：哪些 cpp 组成程序，每个目标需要什么标准；**构建阶段**：配置 → 编译 → 链接，找到第一条错误；**运行排查**：输入、边界、生命周期，断点与合适的检查工具。


## 项目里三个角色

| 文件 | 职责 |
| --- | --- |
| `.hpp` / `.h` | 声明接口，让使用者知道怎么调用 |
| `.cpp` | 定义函数实现 |
| `CMakeLists.txt` | 声明构建目标、源文件、编译要求 |

例如头文件用 `#pragma once` 或 include guard 防止重复包含，声明 `double distance(Point a, Point b);`；实现文件提供函数体；调用者包含头文件，构建目标同时编译实现文件。模板定义通常需要在使用处可见，不照搬普通函数的拆分规则。

## 构建本教程所有示例

先下载并解压 [完整示例包](examples/cpp-examples.zip)，进入包含 CMakeLists.txt 的目录。

通用流程（已装好并配置编译器）：

```text
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build --config Debug
```

Windows UCRT64 工具链如果默认生成器选到了未安装的 Visual Studio，可明确用 MinGW Makefiles，并保证 UCRT64 的 g++ 与 mingw32-make 在 PATH：

```text
cmake -S . -B build-mingw -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Debug
cmake --build build-mingw
```

单配置生成器的程序通常在 build 目录，Visual Studio 等多配置生成器通常在 build/Debug。例如 Windows 运行 `./build-mingw/project.exe`，Linux 运行 `./build/project`。

默认不构建 C++23 示例，便于先完成基础。工具链支持 expected 后，再开启：

```text
cmake -S . -B build -DCPP_TUTORIAL_ENABLE_CPP23=ON
cmake --build build --config Debug
```

不要在已经使用另一生成器的同一个构建目录里换生成器，新建一个目录。

## 构建文件的关键意思

完整 [CMakeLists.txt](examples/CMakeLists.txt) 为每个示例建立独立目标；目标按需使用 17、20、23，设置 `CXX_STANDARD_REQUIRED ON`，避免不支持时悄悄降级，并用 `CXX_EXTENSIONS OFF` 禁用编译器专属标准模式。语义参考 [CMake 官方文档](https://cmake.org/cmake/help/latest/prop_tgt/CXX_STANDARD.html)。线程目标链接 Threads::Threads。

## 调试时先缩小问题

1. 用警告找未使用变量、可疑转换，不要习惯性忽略。
2. 用 `-g -O0` 编译便于调试的 G++ 程序；在断点查看参数、局部变量、调用栈。
3. 先检查空输入、数组下标和悬空引用，再怀疑编译器。
4. 在支持的工具链上用 AddressSanitizer/UndefinedBehaviorSanitizer 检查内存和未定义行为：

```bash
g++ -std=c++20 -g -O1 -fsanitize=address,undefined -fno-omit-frame-pointer project.cpp -o project
./project
```

Sanitizer 是否可用取决于平台和工具链；某些 Windows MinGW 发行版不提供完整支持。它也不是“跑过就证明没有错误”，仍需要输入设计和代码检查。调试版与实际优化版都要进行合适的验证。

## 动手练习

添加一个 `hello.cpp`，在 CMake 中添加目标。故意漏掉定义某个函数的 cpp，观察编译与链接报错的区别。

??? tip "参考答案"

    在构建文件加 `add_executable(hello hello.cpp)`。头文件声明存在但没有函数定义时，单个文件可能编译成功，最终链接会报未定义引用或相应的未解析符号。


---

[返回学习路线](index.md) · [上一章：13 · 并发与线程](concurrency.md) · [下一章：15 · 放牧数据处理小项目 →](project.md)
