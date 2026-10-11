# Q-learning：算法直觉

[算法直觉](q-learning.md) · [公式讲解](../math/q-learning.md) · [Python 实践](../code/q-learning.md)

<span class="rl-badge">异策略 / 表格控制</span>

## 一句话理解

更新时，按照下一步最高的动作分数估计未来。

## 先看这张图

![Q-learning的学习过程示意](../assets/q-learning.svg){ .rl-figure loading=lazy }

[打开图示大图](../assets/q-learning.svg)

图中每个框只展示主要学习关系，完整细节见后面的公式与代码。

## 这几个词是什么意思

**采样策略**：收集经验时怎么选动作。**目标策略**：正在学习其收益的决策规则。Q-learning 的采样可以探索，目标使用贪心选择。

## 用走廊举例

你向右走一步，发现下一位置向右分数高、向左分数低。无论采样策略下一步是否随机向左，更新目标都使用下一位置的最高 Q 值。这样，探索时积累的数据也能用来学习贪心决策的价值。

## 它怎么工作

1. 初始化 Q 表。
2. 用 ε-greedy 选动作，既尝试新动作，也利用已有经验。
3. 记录奖励和下一状态。
4. 用即时奖励加下一状态最高分作为目标，修正当前动作分数。

## “异策略”是什么意思

采样策略可能随机探索，被学习的目标策略却选择最高分动作，两者不同。异策略不是“任何旧数据都永远有效”，仍需要覆盖重要状态与动作，并考虑环境是否变化。

## 优点与限制

更新规则简单，适合小规模离散环境。状态和动作太多时，Q 表存不下，也很难让每格都得到足够训练，DQN 用网络来缓解表格规模问题。

## 在放牧研究里如何理解

可以先把羊群中心所在区域与机器人的相对方位离散化，作为教学环境。但这种离散化会丢失信息，不能直接代表连续场地上的完整放牧问题。

## 检查自己是否看懂

**实际下一动作值为 0.3，最高分为 0.9，更新用哪个？**

??? success "展开答案"

    用 0.9；采样时实际选哪个动作，不改变这里取最大值的规则。


![相同数据下SARSA新Q为0.394，Q-learning新Q为0.502](../assets/sarsa-vs-q.svg){ .rl-figure loading=lazy }

[打开图示大图](../assets/sarsa-vs-q.svg)

## 进一步阅读

[Sutton 与 Barto 教材，第 6 章](https://incompleteideas.net/book/the-book-2nd.html)

[David Silver 对应课程讲义](https://davidstarsilver.wordpress.com/wp-content/uploads/2025/04/lecture-5-model-free-control-.pdf)
