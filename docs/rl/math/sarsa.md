# SARSA：公式讲解

[算法直觉](../intuition/sarsa.md) · [公式讲解](sarsa.md) · [Python 实践](../code/sarsa.md)

先读 [公共符号与回报](index.md)，再看本页。所有数值例子都只用于说明一次更新。

!!! tip "先用一句人话读公式"

    目标 = 奖励 + 折扣 × 实际下一动作的 Q 值；当前 Q 向目标挪一点。


## 核心公式

$$
Q(s_t,a_t)\leftarrow Q(s_t,a_t)+\alpha\left[r_{t+1}+\gamma(1-d_t)Q(s_{t+1},a_{t+1})-Q(s_t,a_t)\right]
$$

## 逐项读懂

- $Q(s,a)$：在状态 $s$ 先做动作 $a$，之后按当前策略行动的预期回报。
- $a_{t+1}$：用当前采样策略实际选出的下一动作。
- 其余结构与 TD 一样：旧估计加学习率乘误差。

## 算一次看看

当前 Q 值为 0.4，奖励为 0.1，下一状态实际选择的动作 Q 值为 0.3，$\gamma=0.9$、$\alpha=0.2$。目标是 0.37，新 Q 值为 $0.4+0.2(0.37-0.4)=0.394$。

即使下一状态另一个动作值为 0.9，SARSA 这次也不使用它，因为实际选择的是值为 0.3 的动作。

## 探索策略

ε-greedy 在概率 $\epsilon$ 下均匀随机选动作，其余时候选最高分动作。若只有一个最高分动作，动作总数为 $m$，该最佳动作的实际概率是 $1-\epsilon+\epsilon/m$，不是简单的 $1-\epsilon$。

## 与代码对照

先计算 `next_action`，再用 `q[ns][next_action]` 更新，最后把它交给下一步真正执行。不能更新用一个动作，执行时又重新随意抽另一个，否则不再对应这里的轨迹。


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
