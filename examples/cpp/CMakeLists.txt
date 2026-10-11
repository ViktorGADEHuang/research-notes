# 要求足够新的 CMake 来配置这个教学项目。
cmake_minimum_required(VERSION 3.20)
# 声明项目使用 C++。
project(cpp_tutorial LANGUAGES CXX)
# C++23 示例默认关闭，兼顾尚未支持 expected 的工具链。
option(CPP_TUTORIAL_ENABLE_CPP23 "Build the C++23 expected example" OFF)
# 查找平台对应的线程链接设置。
find_package(Threads REQUIRED)

# 为每个独立示例建立目标，并设置各自需要的语言标准。
function(add_tutorial name standard)
    add_executable(${name} ${name}.cpp)
    # 要求指定标准且关闭非标准扩展，不支持时直接报错。
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
# 为每个独立示例建立目标，并设置各自需要的语言标准。
endfunction()

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
    add_tutorial(cpp23 23)
endif()
