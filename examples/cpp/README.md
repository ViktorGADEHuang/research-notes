# C++ 教程示例

每个 cpp 是独立程序，使用标准库，不需要 ROS 或额外第三方库。

基础：C++17；cpp20、concurrency、project：C++20；cpp23：C++23。

在已配置编译器的终端：

```
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build --config Debug
```

需要 C++23 时在配置命令加 `-DCPP_TUTORIAL_ENABLE_CPP23=ON`。
Windows MinGW 用户可用 `-G "MinGW Makefiles"`，并把同一工具链的 bin 目录放进 PATH。

也可单独编译：

```
g++ -std=c++20 -Wall -Wextra -Wpedantic project.cpp -o project.exe
./project.exe
```

并发示例 GCC/Clang 增加 `-pthread`。Linux/macOS 可省略 .exe。
输出、解释、练习答案见站点「编程技术 / C++ 与现代 C++」。
放牧小项目仅处理示例数据，不是机器人控制程序。
