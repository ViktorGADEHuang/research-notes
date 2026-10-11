# SARSA：Python 实践

[算法直觉](../intuition/sarsa.md) · [公式讲解](../math/sarsa.md) · [Python 实践](sarsa.md)

## 环境与运行

**语言：Python 3.12 或以上；依赖：仅标准库；实现方式：手写更新。**

环境是一条走廊：非终止状态为 1～5，起点为 3，左端 0 奖励 −1，右端 6 奖励 +1，中间每步奖励 −0.01。动作 0 向左，动作 1 向右。这是帮助理解算法的小环境，不是羊群仿真。

[下载完整 Python 文件](../examples/sarsa.py){ .md-button }

将代码保存为 `sarsa.py`，在文件所在目录运行：

```bash
python sarsa.py
```

也可以从项目根目录运行：

```bash
python docs/rl/examples/sarsa.py
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

q = [[0.0, 0.0] for _ in range(7)]
for _ in range(3000):
    s = 3
    a = choose(q, s)
    while s not in (0, 6):
        ns, reward, done = step(s, a)
        next_action = choose(q, ns) if not done else 0
        target = reward + (0.0 if done else gamma * q[ns][next_action])
        q[s][a] += alpha * (target - q[s][a])
        s, a = ns, next_action  # 下一步执行的就是这个 next_action
print("Q:", [[round(x, 3) for x in row] for row in q[1:6]])
print("Greedy actions:", [max(range(2), key=lambda a: q[s][a]) for s in range(1, 6)])
```

## 对照公式看代码

`next_action` 先选好；Q 更新使用它的分数；下一步沿用同一动作。

## 如何理解输出

输出 Q 表与贪心动作。固定种子与当前设置下，贪心动作应倾向向右；Q 值仍反映持续探索的影响。

## 动手修改

把探索概率从 0.15 改到 0.4，再和 Q-learning 比较数值。

示例不设置人工回合超时，直到真正到达终点。扩展到有时间限制的环境时，要区分真实终止与外部截断。
