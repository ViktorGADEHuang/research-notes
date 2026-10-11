# REINFORCE：Python 实践

[算法直觉](../intuition/reinforce.md) · [公式讲解](../math/reinforce.md) · [Python 实践](reinforce.md)

## 环境与运行

**语言：Python 3.12 或以上；依赖：仅标准库；实现方式：手写更新。**

环境是一条走廊：非终止状态为 1～5，起点为 3，左端 0 奖励 −1，右端 6 奖励 +1，中间每步奖励 −0.01。动作 0 向左，动作 1 向右。这是帮助理解算法的小环境，不是羊群仿真。

[下载完整 Python 文件](../examples/reinforce.py){ .md-button }

将代码保存为 `reinforce.py`，在文件所在目录运行：

```bash
python reinforce.py
```

也可以从项目根目录运行：

```bash
python docs/rl/examples/reinforce.py
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

def softmax(row):
    weights = [math.exp(x - max(row)) for x in row]
    total = sum(weights)
    return [x / total for x in weights]

logits = [[0.0, 0.0] for _ in range(7)]
for _ in range(3000):
    s, episode = 3, []
    while s not in (0, 6):
        probs = softmax(logits[s])
        a = rng.choices([0, 1], weights=probs)[0]
        ns, reward, done = step(s, a)
        episode.append((s, a, reward))
        s = ns
    returns, total = [0.0] * len(episode), 0.0
    for t in reversed(range(len(episode))):
        total = episode[t][2] + gamma * total
        returns[t] = total
    grad = [[0.0, 0.0] for _ in range(7)]
    for t, (s, a, _) in enumerate(episode):
        probs = softmax(logits[s])
        for j in range(2):
            grad[s][j] += gamma**t * returns[t] * ((j == a) - probs[j])
    # 算完一整幕的旧策略梯度后再更新参数。
    for s in range(1, 6):
        for a in range(2):
            logits[s][a] += 0.02 * grad[s][a]
print("P(right):", [round(softmax(logits[s])[1], 3) for s in range(1, 6)])
```

## 对照公式看代码

`logits` 是策略参数；`softmax` 转成动作概率；`grad` 累计回报加权梯度，然后整体更新。

## 如何理解输出

输出各位置向右的概率。右端收益更好，训练后这些概率应明显高于初始的 0.5，但策略依然是随机的。

## 动手修改

降低策略学习率或减少幕数，观察概率变化速度；检查是否对不同种子都能学习。

示例不设置人工回合超时，直到真正到达终点。扩展到有时间限制的环境时，要区分真实终止与外部截断。
