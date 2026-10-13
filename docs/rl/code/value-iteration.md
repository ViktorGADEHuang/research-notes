# 价值迭代：Python 实践

[算法直觉](../intuition/value-iteration.md) · [公式讲解](../math/value-iteration.md) · [Python 实践](value-iteration.md)


!!! tip "读完这页，你应该能做到"

    说明三层循环各做什么，分清新旧价值表，再从分数找到动作编号。

    **先会这些就够了**：已知模型、奖励、价值。

## 看图梳理

![价值迭代 · 代码数据流](../../assets/learning/rl-code-value-iteration.svg){ .learning-figure }

[打开大图](../../assets/learning/rl-code-value-iteration.svg)

**已知模型**：每个动作到哪里，获得多少奖励；**反复更新**：奖励 + 折扣后续价值，各动作中取最大；**得到结果**：最优价值估计，从价值提取贪心动作。


还不认识 Python 的列表、循环或缩进？先查 [Python 阅读入门](../../programming/python-reading.md)，再回来读本页。

## 示例背景

**语言：Python 3.12 或以上；依赖：仅标准库；实现方式：手写更新。**

环境是一条走廊：非终止状态为 1～5，起点为 3，左端 0 奖励 −1，右端 6 奖励 +1，中间每步奖励 −0.01。动作 0 向左，动作 1 向右。这是帮助理解算法的小环境，不是羊群仿真。


本页只提供带注释的代码，按步骤阅读即可，无需创建环境或执行脚本。

## 先读懂一次计算，再读完整循环

下面把“某个位置的两个候选动作”单独拿出来。这里只演示已知数据怎样计算，不是让智能体实际执行两个动作。

```python
# 假设向左、向右后的旧状态价值分别是 0.2、0.8，且均未终止。
old_left, old_right = 0.2, 0.8
reward, gamma = -0.01, 0.95
left_score = reward + gamma * old_left    # -0.01 + 0.19 = 0.18
right_score = reward + gamma * old_right  # -0.01 + 0.76 = 0.75
candidates = [left_score, right_score]     # 列表顺序对应动作 0、1。
new_value = max(candidates)                # 得到分数 0.75。
best_action = max(range(2), key=lambda a: candidates[a])  # 得到动作编号 1。
```

`key=lambda a: candidates[a]` 的意思是“比较动作编号时，按它对应的分数比较”。编号 1 不天然比编号 0 好，只是这个例子里右侧分数更高。

| 完整代码变量 | 内容大小 | 什么时候重建 |
| --- | --- | --- |
| `values` | 7 个数，按位置保存 V | 开始创建一次，跨轮修改 |
| `old` | 上一轮 7 个值的副本 | 每轮开始复制，轮内只读 |
| `candidates` | 当前位置的两个候选分数 | 每换一个位置清空 |
| `policy` | 位置 1～5 的动作编号 | 价值迭代结束后提取 |

先读第一重循环“重复计算”，再读第二重循环“每个位置”，最后读第三重循环“每个动作”。`old = values[:]` 真正复制列表；若写成 `old = values`，两个名字会指向同一张表，就不是这份代码的同步更新了。

## 完整代码

```python title="value-iteration · 完整学习代码"
"""标准库教学代码：对照注释理解更新过程，无需运行。"""

# gamma 给未来奖励打折；价值迭代每轮直接采用最大的动作目标。
gamma = 0.95

# 小走廊模型：输入当前位置与动作，返回下一位置、奖励、终止标记。
def step(state, action):
    # 调用者只传动作 0 或 1；先按动作找到下一位置。
    if action == 1:
        ns = state + 1  # 向右。
    else:
        ns = state - 1  # 向左。
    # 两端才是真正终点；0、6 不再作为下一次 step 的输入。
    done = ns in (0, 6)
    # 奖励描述刚发生的结果；进入终点时不再额外扣中间步进代价。
    if ns == 6:
        reward = 1.0
    elif ns == 0:
        reward = -1.0
    else:
        reward = -0.01
    return ns, reward, done


# V 表按状态存分数；两个终止位置也占位，但不更新它们。
values = [0.0] * 7
# 最多做 10000 轮计算；每轮重算五个位置，不与环境采样交互。
# 这些数量是教学设置，不构成收敛保证。
for _ in range(10000):
    # 复制上一轮的 V；本轮所有目标都使用旧表，进行同步更新。
    # 本表元素是不可变数字，切片得到独立列表，写 values 不会改 old。
    old = values[:]
    for s in range(1, 6):
        candidates = []
        for a in range(2):
            # 用已知规则计算候选动作的结果；这里是在枚举，不是采样。
            ns, reward, done = step(s, a)
            # 比较两种动作的“一步奖励 + 下一状态价值”，不是随机采样。
            candidates.append(reward + (0.0 if done else gamma * old[ns]))
        # 价值迭代选择当前最大的候选目标，逼近最优状态价值。
        values[s] = max(candidates)
    # 比较新旧表的最大变化；足够小则停止迭代。
    if max(abs(x - y) for x, y in zip(values, old)) < 1e-10:
        break
policy = []
for s in range(1, 6):
    candidates = []
    for a in range(2):
        # 用已知规则计算候选动作的结果；这里是在枚举，不是采样。
        ns, reward, done = step(s, a)
        # 比较两种动作的“一步奖励 + 下一状态价值”，不是随机采样。
        candidates.append(reward + (0.0 if done else gamma * values[ns]))
    policy.append(max(range(2), key=lambda a: candidates[a]))
print("Values:", [round(x, 3) for x in values[1:6]])
print("Actions (0=left, 1=right):", policy)
```

## 对照公式看代码

`candidates` 对应每个动作的即时奖励与未来价值；`max` 执行贪心备份；`old` 让本轮使用上一轮价值。

## 如何理解输出

按本页的已知规则，最优走法是在五个非终止位置都向右。可以先独立手算：V(5)=1，V(4)=−0.01+0.95×1=0.94，V(3)=−0.01+0.95×0.94=0.883；再同样倒推位置 2、1。

由模型计算出的保留三位小数的结果是：

```text title="由走廊规则推算的结果"
Values: [0.777, 0.829, 0.883, 0.94, 1.0]
Actions (0=left, 1=right): [1, 1, 1, 1, 1]
```

这份结果可用模型和纸笔核对；不是运行训练后采集的成绩。调用 step 枚举结果也没有采样未知环境。

## 阅读练习：把理解分成三小步

<div class="practice-card" markdown="1">

<p class="practice-kicker">纸笔演算，不需要运行训练</p>

<p class="practice-title">先算分数，再选动作</p>

**沿用这些条件**：未终止，奖励均为 −0.01，折扣 0.95；下一位置旧价值分别为 0.2、0.8。

**从哪里开始**：回到本页的核心短片段，先圈出输入和旧预测，再计算临时目标；最后才判断要修改什么。

**按这几步做**：

1. 分别计算左右两个候选分数。
2. 写出新状态价值与最佳动作编号，约定左 0、右 1。
3. 解释 old 若只指向 values 而非复制，会改变什么。

??? tip "先要一点提示？"

    给每个数写上名字，区分奖励、旧预测、目标、参数或动作。每算完一步，把中间结果写下来，再进入下一步，不只抄最后答案。

??? example "对照完整推理"

    先算左：−0.01 + 0.95×0.2 = 0.18；右：−0.01 + 0.95×0.8 = 0.75。新价值为 0.75，最佳动作编号为 1。分数和编号不是同一种输出。

    old = values 会让两个名字指向同一张可修改列表；本轮已经更新的值可能被本轮后续计算读到，变成原地更新。它可以对应另一种更新安排，但不再是本页用整份上一轮数据的同步版本。

</div>
