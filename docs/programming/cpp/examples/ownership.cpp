#include <iostream>
#include <memory>
#include <utility>

struct Sensor {
    double distance_m;
};

void show(const Sensor& sensor) {
    std::cout << "distance: " << sensor.distance_m << '\n';
}

int main() {
    auto owner = std::make_unique<Sensor>(Sensor{2.5});
    show(*owner);
    auto new_owner = std::move(owner);
    std::cout << std::boolalpha << "old owner empty: " << !owner << '\n';
    show(*new_owner);
    auto shared = std::make_shared<Sensor>(Sensor{1.0});
    std::weak_ptr<Sensor> observer = shared;
    shared.reset();
    std::cout << "resource expired: " << observer.expired() << '\n';
}
