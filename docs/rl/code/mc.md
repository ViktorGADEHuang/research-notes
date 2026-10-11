# 蒙特卡洛（MC）：Python 实践

[算法直觉](../intuition/mc.md) · [公式讲解](../math/mc.md) · [Python 实践](mc.md)

## 环境与运行

**语言：Python 3.12 或以上；依赖：仅标准库；实现方式：手写更新。**

环境是一条走廊：非终止状态为 1～5，起点为 3，左端 0 奖励 −1，右端 6 奖励 +1，中间每步奖励 −0.01。动作 0 向左，动作 1 向右。这是帮助理解算法的小环境，不是羊群仿真。

[下载完整 Python 文件](../examples/mc.py){ .md-button }

将代码保存为 `mc.py`，在文件所在目录运行：

```bash
python mc.py
```

也可以从项目根目录运行：

```bash
python docs/rl/examples/mc.py
```

## 用中文顺着读代码

先看 `step`：它规定“往哪走、得到什么奖励、什么时候结束”。再看存分数的列表或存偏好的 `logits`，最后找更新语句。你可以暂时跳过打印与列表推导式，先对照公式看分数如何改变。

`state` / `s` 是当前位置，`ns` 是下一位置；`done` 表示这局是否真正结束；`gamma` 控制未来奖励打几折。固定随机种子是为了让同一配置更容易复现。

## 完整代码

```python
"""标准库教学示例；运行本文件即可，不需要安装第三方依赖。"""
import math
import random

rng = random.Random(7)
gamma, alpha = 0.95, 0.1

def step(state, action):
    ns = state + (1 if action == 1 else -1)
    done = ns in (0, 6)
    reward = 1.0 if ns == 6 else -1.0 if ns == 0 else -0.01
    return ns, reward, done

def choose(q, state, epsilon=0.15):
    if rng.random() < epsilon:
        return rng.randrange(2)
    best = max(q[state])
    return rng.choice([a for a in range(2) if q[state][a] == best])

values = [0.0] * 7
counts = [0] * 7
for _ in range(10000):
    s, episode = 3, []
    while s not in (0, 6):
        a = rng.randrange(2)  # 只评估随机策略，不改进策略
        ns, reward, done = step(s, a)
        episode.append((s, reward))
        s = ns
    returns, total = [0.0] * len(episode), 0.0
    for t in reversed(range(len(episode))):
        total = episode[t][1] + gamma * total
        returns[t] = total
    visited = set()
    for t, (s, _) in enumerate(episode):
        if s not in visited:
            visited.add(s)
            counts[s] += 1
            values[s] += (returns[t] - values[s]) / counts[s]
print("Random-policy values:", [round(x, 3) for x in values[1:6]])
```

## 对照公式看代码

从回合结尾反向计算 `returns`；`visited` 只统计第一次访问；`counts` 让更新等价于历史回报均值。

## 如何理解输出

输出均匀随机策略下的价值，而不是最优价值。右侧通常为正，左侧通常为负，中间还受到每步代价影响。

## 动手修改

比较 100、1000 与 10000 幕结果；固定环境后多换几个种子，观察估计波动。

示例不设置人工回合超时，直到真正到达终点。扩展到有时间限制的环境时，要区分真实终止与外部截断。
