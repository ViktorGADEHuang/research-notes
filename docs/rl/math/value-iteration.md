# 价值迭代：公式讲解

[算法直觉](../intuition/value-iteration.md) · [公式讲解](value-iteration.md) · [Python 实践](../code/value-iteration.md)

先读 [公共符号与回报](index.md)，再看本页。所有数值例子都只用于说明一次更新。

!!! tip "先用一句人话读公式"

    枚举动作 → 按发生概率平均各结果 → 取最高分 → 更新状态分数。


## 核心公式

$$
V_{k+1}(s)=\max_a\sum_{s',r}p(s',r\mid s,a)\left[r+\gamma V_k(s')\right]
$$

## 逐项读懂

- $V_k(s)$：第 $k$ 轮时，对状态 $s$ 的长期收益估计。
- $p(s',r\mid s,a)$：做动作 $a$ 后，出现下一状态 $s'$ 与奖励 $r$ 的概率。这是已知模型。
- $r+\gamma V_k(s')$：眼前奖励，加上打折后的后续价值。
- 求和：把所有可能结果按发生概率加权，不只看一种结果。
- $\max_a$：算完各动作的期望后，选择最高的。

## 算一次看看

动作 A 的奖励为 −0.01，下一位置价值为 0.8，折扣为 0.95；目标为 0.75。动作 B 的下一位置价值为 0.2，相同奖励下目标为 0.18。本轮当前状态的新价值取 0.75。

## 如何得到策略

$$
\pi(s)\in\arg\max_a\sum_{s',r}p(s',r\mid s,a)[r+\gamma V(s')]
$$

$\arg\max$ 返回使分数最大的动作；$\max$ 返回分数本身。多个动作并列时，可以选择其中一个。

## 与代码对照

代码中 `targets` 保存两个动作的目标，`max(targets)` 就是价值迭代。`old` 是上一轮价值的拷贝，使本轮使用同一批旧估计。终止状态的未来价值为零。本例是确定性模型，因此求和退化为一个结果。

## 进一步阅读

[Sutton 与 Barto 教材，第 4 章](https://incompleteideas.net/book/the-book-2nd.html)

[David Silver 对应课程讲义](https://davidstarsilver.wordpress.com/wp-content/uploads/2025/04/lecture-3-planning-by-dynamic-programming-.pdf)
