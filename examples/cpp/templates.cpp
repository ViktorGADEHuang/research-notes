#include <iostream>
#include <type_traits>

// T 是编译期类型参数，可复用同一份配方。
template<typename T>
// 满足常量表达式要求时可在编译期求值，也可运行时计算。
constexpr T square(T value) {
    // 要求类型支持乘法；整数溢出仍需另外考虑。
    return value * value;
}

// 这里根据 T 的类别选择输出格式，数值仍由每次调用传入。
template<typename T>
void describe(T value) {
    // 按类型选择分支，在模板实例化时丢弃另一分支。
    if constexpr (std::is_integral_v<T>) {
        std::cout << "integer: " << value << '\n';
    } else {
        // 本例传入 double；else 本身并不保证任意 T 都是数值类型。
        std::cout << "other number: " << value << '\n';
    }
}

// 程序入口；下面按顺序执行示例步骤。
int main() {
    // 编译时检查结论；条件不满足时无法生成程序。
    static_assert(square(3) == 9);
    // 先调用 square 得到 9，再把这个 int 结果交给 describe。
    describe(square(3));
    // 1.5 使 T 推导为 double，返回 2.25，走非整数分支。
    describe(square(1.5));
}
