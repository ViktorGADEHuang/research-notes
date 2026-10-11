# 时序差分 TD(0)：Python 实践

[算法直觉](../intuition/td.md) · [公式讲解](../math/td.md) · [Python 实践](td.md)


!!! tip "读完这页，你应该能做到"

    找到输入、目标或训练调用，再对照公式解释关键注释。

    **先会这些就够了**：下一状态价值、学习率。


## 看图梳理

![TD(0) · 代码数据流](../../assets/learning/rl-code-td.svg){ .learning-figure }

[打开大图](../../assets/learning/rl-code-td.svg)

**走一步**：状态 → 动作 → 奖励，观察下一状态；**构造目标**：奖励 + 折扣 V 下一步，真正终止时无后续项；**立即修正**：计算 TD 误差，旧值 + 步长 × 误差。


还不认识 Python 的列表、循环或缩进？先查 [Python 阅读入门](../../programming/python-reading.md)，再回来读本页。

## 示例背景

**语言：Python 3.12 或以上；依赖：仅标准库；实现方式：手写更新。**

环境是一条走廊：非终止状态为 1～5，起点为 3，左端 0 奖励 −1，右端 6 奖励 +1，中间每步奖励 −0.01。动作 0 向左，动作 1 向右。这是帮助理解算法的小环境，不是羊群仿真。

[下载完整 Python 文件](../examples/td.py){ .md-button }

本页只提供带注释的代码，按步骤阅读即可，无需创建环境或执行脚本。

## 用中文顺着读代码

先看 step 的三个返回值，再圈出 target 与 values[s] 的修改。每一步只更新刚离开的状态，然后才把 s 推进到 ns。

`state` / `s` 是当前位置，`ns` 是下一位置；`done` 表示这局是否真正结束；`gamma` 控制未来奖励打几折。固定随机种子是为了让同一配置更容易复现。

## 一次循环里，哪几个值先后改变

只看 `s = 3`、动作向右这一次：step 先交回 ns = 4、reward = −0.01、done = False。若 values[4] = 0.8，target 得到 0.75；若 values[3] = 0.3、alpha = 0.1，则修改后为 0.345。

更新时 s 还必须是 3，因为改的是刚离开的位置。最后才执行 `s = ns`，把当前位置推进到 4。如果先改 s，再拿 s 当下标更新，就会改错格子。

下一幕不会清空 values，它要跨回合累积经验；每幕只把当前位置重新设为 3。看清哪些数据重置、哪些数据保留，是理解循环的关键。

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


# V 表按状态存分数；两个终止位置也占位，但不更新它们。
values = [0.0] * 7
# 外层控制迭代或采样幕数；数值只是教学配置，不是收敛保证。
for _ in range(10000):
    s = 3
    # 持续与环境交互，直到走到左端或右端。
    while s not in (0, 6):
        a = rng.randrange(2)  # 与 MC 使用同一随机策略
        # 执行一次动作，获得下一状态、奖励和真正终止的标记。
        ns, reward, done = step(s, a)
        # 目标 = 本步奖励 + 折扣后的后续估计；done 时后续项归零。
        target = reward + (0.0 if done else gamma * values[ns])
        # TD 每走一步就更新 V，无需等到这一幕结束。
        values[s] += alpha * (target - values[s])
        s = ns
print("Random-policy values:", [round(x, 3) for x in values[1:6]])
```

## 对照公式看代码

`target` 使用下一状态旧价值；`alpha` 控制更新幅度；真正终止时未来项为零。

## 如何理解输出

输出随机策略价值。因为使用固定学习率，最终估计仍可能波动，不会与 MC 数值完全一样。

## 阅读练习：不用运行，也能推演

<div class="practice-card" markdown="1">

<p class="practice-kicker">把代码与公式接起来</p>

<p class="practice-title">先识别终止，再算一步目标</p>

正文的下一状态还有价值。现在改为真正终止，检查代码怎样去掉后续项。

**沿用这些条件**：当前 V 为 0.4，奖励为 1，学习率为 0.2，done 为 True。

**你的任务**：读 target 的条件表达式，手算目标与新 V；不运行循环。

??? example "查看推演与解释"

    目标为 1；新 V 为 0.4 + 0.2 × (1 − 0.4) = 0.52。

</div>
