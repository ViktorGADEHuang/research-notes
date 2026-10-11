#include <iostream>
#include <memory>
#include <utility>
#include <vector>

int main() {
    std::vector<int> original{1, 2, 3};
    auto copy = original;
    copy[0] = 9;
    std::cout << "original first: " << original[0] << '\n';
    std::cout << "copy first: " << copy[0] << '\n';
    auto moved = std::move(original);
    std::cout << "moved size: " << moved.size() << '\n';
    original.clear(); // Valid regardless of its unspecified contents.
    original.push_back(7);
    std::cout << "reused original: " << original[0] << '\n';
    auto owner = std::make_unique<int>(42);
    auto recipient = std::move(owner);
    std::cout << "recipient: " << *recipient << '\n';
}
