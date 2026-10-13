# C++ 教程示例

每个 cpp 是独立程序，使用标准库，不需要 ROS 或额外第三方库。

基础：C++17；cpp20、concurrency、project：C++20；cpp23：C++23。

这些源文件供本地维护，网站只展示带注释的代码。进入本目录后，在已配置编译器的终端中选择与你的工具链对应的配置方式。

Windows UCRT64 / G++，使用单配置生成器：

```
cmake -S . -B build -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Debug
cmake --build build
```

同一工具链的 bin 目录要在 PATH 中，以便配置、编译和运行都找到相应工具与 DLL。Linux/macOS 使用已安装的 Make 或 Ninja 单配置生成器时，可省略 `-G "MinGW Makefiles"`。

若使用 Visual Studio 多配置生成器，使用单独的 build-vs 目录：

```
cmake -S . -B build-vs
cmake --build build-vs --config Debug
```

配置日志必须确认选到 Visual Studio；其默认程序位置通常是 build-vs/Debug/目标名.exe。多配置用 --config 选择配置，CMAKE_BUILD_TYPE 只负责单配置生成器。

需要 C++23 时在配置命令加 `-DCPP_TUTORIAL_ENABLE_CPP23=ON`；编译器与标准库仍需实现 expected 等所用功能。

也可单独编译：

```
g++ -std=c++20 -Wall -Wextra -Wpedantic project.cpp -o project.exe
./project.exe
```

并发示例 GCC/Clang 增加 `-pthread`。Linux/macOS 可省略 .exe。
输出、解释、练习答案见站点「编程技术 / C++ 与现代 C++」。
放牧小项目仅处理示例数据，不是机器人控制程序。
