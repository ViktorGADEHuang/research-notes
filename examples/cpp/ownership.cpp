#include <iostream>
#include <memory>
#include <utility>

// 简单数据对象，成员默认公开。
struct Sensor {
    double distance_m;
};

// 这里只借用传感器，不获得销毁它的责任。
void show(const Sensor& sensor) {
    std::cout << "distance: " << sensor.distance_m << '\n';
}

// 程序入口；下面按顺序执行示例步骤。
int main() {
    // 创建资源并交给唯一拥有者，离开作用域自动释放。
    auto owner = std::make_unique<Sensor>(Sensor{2.5});
    // *owner 取得那个 Sensor，show 用只读引用暂时借看它。
    show(*owner);
    // 转移 unique_ptr 所有权；之后原 owner 保证为空。
    auto new_owner = std::move(owner);
    std::cout << std::boolalpha << "old owner empty: " << !owner << '\n';
    show(*new_owner);
    // 共享所有权：最后一个强拥有者离开时销毁对象。
    // 这里另建一个 Sensor，与上面的 unique_ptr 资源互不相同。
    auto shared = std::make_shared<Sensor>(Sensor{1.0});
    // 弱观察者不延长资源的生命周期。
    std::weak_ptr<Sensor> observer = shared;
    // 释放这里最后一个强拥有者，传感器随之销毁。
    shared.reset();
    // expired 只用于本例展示状态；真正访问对象应调用 lock 并检查结果。
    std::cout << "resource expired: " << observer.expired() << '\n';
}
