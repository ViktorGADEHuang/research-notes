#include <atomic>
#include <iostream>
#include <thread>

int main() {
    std::atomic<int> samples{0};
    {
        const auto collect = [&samples] {
            for (int i = 0; i < 1000; ++i) {
                samples.fetch_add(1); // Default sequentially consistent ordering.
            }
        };
        std::jthread first{collect};
        std::jthread second{collect};
    } // Both jthreads join before reading the final count.
    std::cout << "samples: " << samples.load() << '\n';
}
