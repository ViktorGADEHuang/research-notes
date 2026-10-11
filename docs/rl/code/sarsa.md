# SARSA：Python 实践

[算法直觉](../intuition/sarsa.md) · [公式讲解](../math/sarsa.md) · [Python 实践](sarsa.md)


!!! tip "读完这页，你应该能做到"

    找到输入、目标或训练调用，再对照公式解释关键注释。

    **先会这些就够了**：Q 表、epsilon-greedy。


## 看图梳理

![SARSA · 代码数据流](../../assets/learning/rl-code-sarsa.svg){ .learning-figure }

[打开大图](../../assets/learning/rl-code-sarsa.svg)

**当前策略采样**：执行动作 a，在下一状态选 a 下一步；**用实际动作估计**：奖励 + 折扣 Q 下一步，下一步按该动作执行；**更新一格 Q**：目标减去旧 Q，属于同策略学习。


## 示例背景

**语言：Python 3.12 或以上；依赖：仅标准库；实现方式：手写更新。**

环境是一条走廊：非终止状态为 1～5，起点为 3，左端 0 奖励 −1，右端 6 奖励 +1，中间每步奖励 −0.01。动作 0 向左，动作 1 向右。这是帮助理解算法的小环境，不是羊群仿真。

[下载完整 Python 文件](../examples/sarsa.py){ .md-button }

本页只提供带注释的代码，按步骤阅读即可，无需创建环境或执行脚本。

## 用中文顺着读代码

先看 `step`：它规定“往哪走、得到什么奖励、什么时候结束”。再看存分数的列表或存偏好的 `logits`，最后找更新语句。你可以暂时跳过打印与列表推导式，先对照公式看分数如何改变。

`state` / `s` 是当前位置，`ns` 是下一位置；`done` 表示这局是否真正结束；`gamma` 控制未来奖励打几折。固定随机种子是为了让同一配置更容易复现。

## 完整代码

```python
"""标准库教学代码：对照注释理解更新过程，无需运行。"""
import random

# 固定随机数起点，便于对照不同步骤；随机种子不保证跨硬件完全一致。
rng = random.Random(7)
# gamma 给未来奖励打折；alpha 决定每次向目标修正多少。
gamma, alpha = 0.95, 0.1

# 小走廊模型：输入当前位置与动作，返回下一位置、奖励、终止标记。
def step(state, action):
    # 动作 1 向右一步，动作 0 向左一步。
    ns = state + (1 if action == 1 else -1)
    # 走到两端才是真正终止；终止状态没有后续奖励。
    done = ns in (0, 6)
    # 右端奖励 +1、左端 -1，其余每步 -0.01，鼓励尽快到达右端。
    reward = 1.0 if ns == 6 else -1.0 if ns == 0 else -0.01
    return ns, reward, done

# epsilon-greedy：少量随机探索，多数时候选择当前高分动作。
def choose(q, state, epsilon=0.15):
    # 以 epsilon 的概率探索，防止一直停在当前看起来最好的选择。
    if rng.random() < epsilon:
        return rng.randrange(2)
    # 取当前状态的最高 Q 值；相同分数的动作随机打破平局。
    best = max(q[state])
    return rng.choice([a for a in range(2) if q[state][a] == best])

# Q 表每行对应状态，两列分别对应向左与向右。
q = [[0.0, 0.0] for _ in range(7)]
# 外层控制迭代或采样幕数；数值只是教学配置，不是收敛保证。
for _ in range(3000):
    s = 3
    a = choose(q, s)
    # 持续与环境交互，直到走到左端或右端。
    while s not in (0, 6):
        # 执行一次动作，获得下一状态、奖励和真正终止的标记。
        ns, reward, done = step(s, a)
        # SARSA 用下一步实际准备执行的动作；终止时的占位动作不参与目标。
        next_action = choose(q, ns) if not done else 0
        # 目标 = 本步奖励 + 折扣后的后续估计；done 时后续项归零。
        target = reward + (0.0 if done else gamma * q[ns][next_action])
        # Q 更新：旧值 + 学习率 ×（目标 - 旧值），只改刚执行的状态动作格。
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
