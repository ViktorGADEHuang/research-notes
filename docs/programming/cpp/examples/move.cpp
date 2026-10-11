#include <iostream>
#include <memory>
#include <utility>
#include <vector>

// 程序入口；下面按顺序执行示例步骤。
int main() {
    std::vector<int> original{1, 2, 3};
    // 复制出独立容器，修改副本不影响原列表。
    auto copy = original;
    // 只修改副本的第一个元素。
    copy[0] = 9;
    std::cout << "original first: " << original[0] << '\n';
    // 只修改副本的第一个元素。
    std::cout << "copy first: " << copy[0] << '\n';
    // std::move 允许移动构造，实际转移由 vector 完成。
    auto moved = std::move(original);
    std::cout << "moved size: " << moved.size() << '\n';
    // 不依赖移动后内容；先清空，再把源对象用于新数据。
    original.clear(); // Valid regardless of its unspecified contents.
    // 移动后的 vector 仍有效，可重新使用。
    original.push_back(7);
    std::cout << "reused original: " << original[0] << '\n';
    auto owner = std::make_unique<int>(42);
    // unique_ptr 禁止复制，但可移动转交资源。
    auto recipient = std::move(owner);
    std::cout << "recipient: " << *recipient << '\n';
}
