# 这是 CMake 的最低版本要求，不是 C++ 语言标准的版本号。
cmake_minimum_required(VERSION 3.20)
# 为整个项目命名；CXX 表示只查找 C++ 编译器。
project(cpp_tutorial LANGUAGES CXX)
# C++23 示例默认关闭，兼顾尚未支持 expected 的工具链。
option(CPP_TUTORIAL_ENABLE_CPP23 "Build the C++23 expected example" OFF)
# 查找平台对应的线程链接设置。
find_package(Threads REQUIRED)

# 自定义函数：name 是程序名，standard 是它使用的 C++ 标准版本。
function(add_tutorial name standard)
    # 例如 name=basics 时，下面等价于 add_executable(basics basics.cpp)。
    add_executable(${name} ${name}.cpp)
    # 要求指定标准模式，不允许回退到更旧标准，并关闭扩展模式。
    set_target_properties(${name} PROPERTIES
        CXX_STANDARD ${standard}
        CXX_STANDARD_REQUIRED ON
        CXX_EXTENSIONS OFF)
    if(MSVC)
        # 开启常见警告，帮助发现可疑代码。
        target_compile_options(${name} PRIVATE /W4 /utf-8)
    else()
        # 开启常见警告，帮助发现可疑代码。
        target_compile_options(${name} PRIVATE -Wall -Wextra -Wpedantic)
    endif()
endfunction()

# 调用上面定义的函数；每个文件各有一个 main，不能合成一个程序。
add_tutorial(basics 17)
add_tutorial(functions 17)
add_tutorial(classes 17)
add_tutorial(containers 17)
add_tutorial(ownership 17)
add_tutorial(templates 17)
add_tutorial(lambdas 17)
add_tutorial(move 17)
add_tutorial(cpp17 17)
add_tutorial(cpp20 20)
add_tutorial(concurrency 20)
add_tutorial(project 20)
# 线程示例使用平台提供的线程支持。
target_link_libraries(concurrency PRIVATE Threads::Threads)
if(CPP_TUTORIAL_ENABLE_CPP23)
    # 只有明确启用开关，才把这个示例加入构建；仍需工具链支持 expected。
    add_tutorial(cpp23 23)
endif()
