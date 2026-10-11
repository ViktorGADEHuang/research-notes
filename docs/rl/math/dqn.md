# DQN：公式讲解

[算法直觉](../intuition/dqn.md) · [公式讲解](dqn.md) · [Python 实践](../code/dqn.md)

先读 [公共符号与回报](index.md)，再看本页。所有数值例子都只用于说明一次更新。

!!! tip "先用一句人话读公式"

    学习目标 = 奖励 + 折扣 × 目标网络的下一状态最高分；训练当前网络去接近目标。



## 看图梳理

![DQN · 公式关系](../../assets/learning/rl-math-dqn.svg){ .learning-figure }

[打开大图](../../assets/learning/rl-math-dqn.svg)

**收集与存经验**：状态、动作、奖励，经验回放池；**构造稳定目标**：目标网络估计最大 Q，终止时屏蔽后续项；**训练 Q 网络**：减小预测与目标差，梯度与同步由库实现。


## 把表换成网络

$$
y=r+\gamma(1-d)\max_{a'}Q_{\bar\theta}(s',a')
$$

$$
L(\theta)=\mathbb E_{(s,a,r,s',d)\sim\mathcal D}\left[(Q_\theta(s,a)-y)^2\right]
$$

## 逐项读懂

- $\theta$：正在训练的 Q 网络参数；$\bar\theta$：目标网络参数。
- $\mathcal D$：经验回放池，存储状态转移。
- $y$：使用目标网络计算的目标；训练当前网络时把它当常量。
- 平方误差：预测偏离目标越远，惩罚越大。
- $\mathbb E$：对回放样本的平均，实际用小批量近似。

## 算一次看看

奖励为 1、没有终止、下一状态目标网络最高分为 2、折扣 0.9，则 $y=2.8$。当前网络对采样动作预测 1.5，则单样本平方误差为 $(1.5-2.8)^2=1.69$。

## 目标网络何时更新

原始思路是隔一段时间复制参数：$\bar\theta\leftarrow\theta$。这样目标不在每次梯度更新时同步剧烈变化。

## 与代码对照

训练脚本用 SB3 执行真实 DQN 更新，不是手写完整网络。`buffer_size` 对应回放容量，`target_update_interval` 对应同步间隔。上式是便于理解的平方损失，SB3 的 DQN 实现采用 Huber 损失与梯度裁剪。它不包含 Double DQN：后者把选动作与评估动作拆开，目标公式不同。

## 进一步阅读

[DQN 原始论文](https://arxiv.org/abs/1312.5602)
