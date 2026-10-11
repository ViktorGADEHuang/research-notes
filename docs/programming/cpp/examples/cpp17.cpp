#include <iostream>
#include <map>
#include <optional>
#include <string>
#include <string_view>
#include <variant>

std::optional<double> lookup(const std::map<int, double>& positions, int id) {
    if (const auto it = positions.find(id); it != positions.end()) {
        return it->second;
    }
    return std::nullopt;
}

int main() {
    const std::map<int, double> positions{{1, 0.0}, {2, 3.5}};
    for (const auto& [id, x] : positions) {
        std::cout << "sheep " << id << ": " << x << '\n';
    }
    std::cout << "missing fallback: " << lookup(positions, 9).value_or(-1.0) << '\n';
    if (auto x = lookup(positions, 1)) {
        std::cout << "valid zero: " << *x << '\n';
    }
    const std::string name{"herding"};
    const std::string_view view{name};
    std::cout << "view: " << view << '\n';
    const std::variant<int, std::string> message{std::string{"ready"}};
    std::visit([](const auto& value) { std::cout << value << '\n'; }, message);
}
