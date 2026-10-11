# Q-learning：Python 实践

[算法直觉](../intuition/q-learning.md) · [公式讲解](../math/q-learning.md) · [Python 实践](q-learning.md)


!!! tip "读完这页，你应该能做到"

    找到输入、目标或训练调用，再对照公式解释关键注释。

    **先会这些就够了**：Q 表、贪心选择。


## 看图梳理

![Q-learning · 代码数据流](../../assets/learning/rl-code-q-learning.svg){ .learning-figure }

[打开大图](../../assets/learning/rl-code-q-learning.svg)

**行为策略采样**：随机探索或贪心，得到奖励和下一状态；**目标用最大 Q**：不依赖实际下一动作，真正终止无后续项；**更新一格 Q**：学习贪心目标策略，属于异策略学习。


## 示例背景

**语言：Python 3.12 或以上；依赖：仅标准库；实现方式：手写更新。**

环境是一条走廊：非终止状态为 1～5，起点为 3，左端 0 奖励 −1，右端 6 奖励 +1，中间每步奖励 −0.01。动作 0 向左，动作 1 向右。这是帮助理解算法的小环境，不是羊群仿真。

[下载完整 Python 文件](../examples/q-learning.py){ .md-button }

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
    # 持续与环境交互，直到走到左端或右端。
    while s not in (0, 6):
        a = choose(q, s)
        # 执行一次动作，获得下一状态、奖励和真正终止的标记。
        ns, reward, done = step(s, a)
        # 目标 = 本步奖励 + 折扣后的后续估计；done 时后续项归零。
        target = reward + (0.0 if done else gamma * max(q[ns]))
        # Q 更新：旧值 + 学习率 ×（目标 - 旧值），只改刚执行的状态动作格。
        q[s][a] += alpha * (target - q[s][a])
        s = ns
print("Q:", [[round(x, 3) for x in row] for row in q[1:6]])
print("Greedy actions:", [max(range(2), key=lambda a: q[s][a]) for s in range(1, 6)])
```

## 对照公式看代码

`max(q[ns])` 是下一状态的最高分；选动作时仍然随机探索。这对应采样策略与目标策略不同。

## 如何理解输出

输出 Q 表与贪心动作。当前设置下，五个状态应学到向右；这不表示所有环境都能用 3000 幕学会。

## 阅读练习：不用运行，也能推演

<div class="practice-card" markdown="1">

<p class="practice-kicker">把代码与公式接起来</p>

<p class="practice-title">同一条经验，比较两种目标</p>

正文的 max 与实际下一动作可能不同。先用相同数字比较目标，不急着改整个算法。

**沿用这些条件**：奖励 0.1，折扣 0.9；下一 Q 为 0.3、0.9，实际下一动作选中 0.3。

**你的任务**：分别写 Q-learning 与 SARSA 的目标；若要改代码，再读 SARSA 页完整的动作衔接。

??? example "查看推演与解释"

    Q-learning 为 0.91，SARSA 为 0.37。只替换 max 而没选择和沿用 next_action，不是完整的 SARSA 修改。

</div>
