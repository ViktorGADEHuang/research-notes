#include <iostream>
#include <map>
#include <optional>
#include <string>
#include <string_view>
#include <variant>

// 返回可选位置：0.0 是有效值，空 optional 才是没找到。
std::optional<double> lookup(const std::map<int, double>& positions, int id) {
    // 只查询不插入，避免 positions[id] 意外添加键。
    if (const auto it = positions.find(id); it != positions.end()) {
        return it->second;
    }
    // 返回“没有结果”，不要把缺失数据当作有效的零值。
    return std::nullopt;
}

// 程序入口；下面按顺序执行示例步骤。
int main() {
    const std::map<int, double> positions{{1, 0.0}, {2, 3.5}};
    // 结构化绑定拆出键和值，并以引用避免复制。
    for (const auto& [id, x] : positions) {
        // 把结果输出到终端，便于与正文中的示例结果对照。
        std::cout << "sheep " << id << ": " << x << '\n';
    }
    // 把结果输出到终端，便于与正文中的示例结果对照。
    std::cout << "missing fallback: " << lookup(positions, 9).value_or(-1.0) << '\n';
    // 检查有没有值，而不是里面的数是不是非零。
    if (auto x = lookup(positions, 1)) {
        // 把结果输出到终端，便于与正文中的示例结果对照。
        std::cout << "valid zero: " << *x << '\n';
    }
    const std::string name{"herding"};
    // 只借看 name 的字符，name 必须保持有效。
    const std::string_view view{name};
    // 把结果输出到终端，便于与正文中的示例结果对照。
    std::cout << "view: " << view << '\n';
    // 当前保存一种类型，不是同时存两种结果。
    const std::variant<int, std::string> message{std::string{"ready"}};
    // 根据 variant 当前类型调用可接受它的 Lambda。
    std::visit([](const auto& value) { std::cout << value << '\n'; }, message);
}
