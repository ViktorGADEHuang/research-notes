#include <atomic>
#include <iostream>
#include <thread>

// 程序入口；下面按顺序执行示例步骤。
int main() {
    // 共享计数器，用原子操作避免竞争导致的丢失更新。
    std::atomic<int> samples{0};
    {
        // 引用捕获计数器；计数器必须比工作线程活得久。
        const auto collect = [&samples] {
            for (int i = 0; i < 1000; ++i) {
                // 原子的读—改—写，默认使用顺序一致的内存序。
                samples.fetch_add(1);
            }
        };
        // 启动工作；对象析构会请求停止并等待线程结束。
        std::jthread first{collect};
        // 再启动一份相同工作，两份工作借用同一个 samples。
        std::jthread second{collect};
    } // 先等待 second，再等待 first；两份工作都结束后才往下走。
    // 内部作用域已结束，两个线程完成后读取最终计数。
    std::cout << "samples: " << samples.load() << '\n';
}
