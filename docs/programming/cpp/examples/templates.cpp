#include <iostream>
#include <type_traits>

template<typename T>
constexpr T square(T value) {
    return value * value;
}

template<typename T>
void describe(T value) {
    if constexpr (std::is_integral_v<T>) {
        std::cout << "integer: " << value << '\n';
    } else {
        std::cout << "other number: " << value << '\n';
    }
}

int main() {
    static_assert(square(3) == 9);
    describe(square(3));
    describe(square(1.5));
}
