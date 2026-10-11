# Q-learning：公式讲解

[算法直觉](../intuition/q-learning.md) · [公式讲解](q-learning.md) · [Python 实践](../code/q-learning.md)

先读 [公共符号与回报](index.md)，再看本页。所有数值例子都只用于说明一次更新。

!!! tip "先用一句人话读公式"

    目标 = 奖励 + 折扣 × 下一状态的最大 Q 值；当前 Q 向目标挪一点。


## 核心公式

$$
Q(s_t,a_t)\leftarrow Q(s_t,a_t)+\alpha\left[r_{t+1}+\gamma(1-d_t)\max_{a'}Q(s_{t+1},a')-Q(s_t,a_t)\right]
$$

## 逐项读懂

唯一关键变化是 $\max_{a'}$：不是用实际下一动作的 Q 值，而是用下一状态中最高的 Q 值。它在估计“接下来按贪心策略行动”的收益。

$a'$ 是用于枚举下一状态动作的占位符，和当前动作 $a_t$ 不是同一个变量。

## 算一次看看

当前 Q 值为 0.4，奖励为 0.1，下一状态动作值分别为 0.3 与 0.9，折扣 0.9，学习率 0.2。目标为 $0.1+0.9\times0.9=0.91$，新值为 0.502。同样数据下，SARSA 若选中较低分动作，目标只有 0.37。

## 最大值与最大动作

训练更新用 `max(q[next_state])` 获取最高分；选动作则需要找到这个最高分属于哪个动作。并列时，示例随机打破平局，避免总是偏向第一个动作。

## 与代码对照

`target` 里的 `max(q[ns])` 对应公式中的最大值；`done` 时目标只保留即时奖励。表格方法的经典收敛结论有访问覆盖与学习率等条件，不代表任意常数学习率、有限训练或神经网络版本都能得到最优解。


![相同数据下SARSA新Q为0.394，Q-learning新Q为0.502](../assets/sarsa-vs-q.svg){ .rl-figure loading=lazy }

[打开图示大图](../assets/sarsa-vs-q.svg)

## 自己算一次

<div class="rl-calculator" data-rl-calculator="compare">
<p class="rl-calculator-title">拖动数字，观察一次更新</p>
<div class="rl-controls">
<label>当前旧估计 <output data-display="current">0.4</output><input type="range" data-value="current" aria-label="当前旧估计" min="-1" max="2" step="0.01" value="0.4"></label>
<label>本次奖励 <output data-display="reward">0.1</output><input type="range" data-value="reward" aria-label="本次奖励" min="-1" max="1" step="0.01" value="0.1"></label>
<label>实际下一动作的 Q 值 <output data-display="next">0.3</output><input type="range" data-value="next" aria-label="实际下一动作的 Q 值" min="-1" max="2" step="0.01" value="0.3"></label>
<label>另一个下一动作的 Q 值 <output data-display="other">0.9</output><input type="range" data-value="other" aria-label="另一个下一动作的 Q 值" min="-1" max="2" step="0.01" value="0.9"></label>
<label>折扣因子 <output data-display="gamma">0.9</output><input type="range" data-value="gamma" aria-label="折扣因子" min="0" max="1" step="0.01" value="0.9"></label>
<label>学习率 <output data-display="alpha">0.2</output><input type="range" data-value="alpha" aria-label="学习率" min="0" max="1" step="0.01" value="0.2"></label>
</div>
<label class="rl-terminal"><input type="checkbox" data-value="terminal"> 下一状态真正终止</label>
<div class="rl-calculation" aria-live="polite"><p data-sarsa>SARSA：目标 0.37 → 新 Q 0.394</p><p data-qlearning>Q-learning：目标 0.91 → 新 Q 0.502</p></div>
<p data-explanation>这是一次更新的演示；滑块改变输入，不会训练机器人。</p>
<noscript>当前显示默认值。启用浏览器 JavaScript 后可拖动滑块。</noscript>
</div>

## 进一步阅读

[Sutton 与 Barto 教材，第 6 章](https://incompleteideas.net/book/the-book-2nd.html)

[David Silver 对应课程讲义](https://davidstarsilver.wordpress.com/wp-content/uploads/2025/04/lecture-5-model-free-control-.pdf)
