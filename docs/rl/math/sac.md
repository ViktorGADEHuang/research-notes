# SAC：公式讲解

[算法直觉](../intuition/sac.md) · [公式讲解](sac.md) · [Python 实践](../code/sac.md)

先读 [公共符号与回报](index.md)，再看本页。所有数值例子都只用于说明一次更新。

!!! tip "先用一句人话读公式"

    Critic 学习“奖励 + 折扣后的未来评分与熵”；Actor 同时追求高 Q 与策略熵；温度决定两者怎么权衡。



!!! tip "读完这页，你应该能做到"

    算出带熵项的目标，区分概率与概率密度。

    **先会这些就够了**：双 Q、随机策略；熵可先按“分布的分散程度”理解。


## 看图梳理

![SAC · 公式关系](../../assets/learning/rl-math-sac.svg){ .learning-figure }

[打开大图](../../assets/learning/rl-math-sac.svg)

**随机策略采样**：连续动作概率密度，经验回放；**奖励与熵目标**：兼顾回报和探索，双 Q 帮助减少偏差；**更新策略与价值**：Actor、Critic 分别优化，auto 可调熵温度。


## 先补熵项，再折扣，最后加眼前奖励

目标中的 `−β log π` 是熵相关项的一次采样。对数密度若为 −0.7，温度 0.2，这一项是 +0.14；加到较小 Q = 1.5 上，得到软价值 1.64。再乘 0.9 得 1.476，最后加本步奖励 −1，目标为 0.476。

这里 log π 为负只是算例条件，不是所有连续密度都如此。密度大于 1 时 log π 可以为正，因此不能把熵项一律当作永远加正分的“额外奖励”。

Critic 学这个软目标；Actor 最小化“温度乘对数密度减 Q”的损失。两处都与熵相关，但它们更新不同参数。先能沿目标路径完成上述算术，再研究采样梯度与 tanh 变换修正。

## 回报里加上熵

$$
J(\pi)=\mathbb E\left[\sum_t\gamma^t\left(r_{t+1}+\beta\,\mathcal H(\pi(\cdot\mid s_t))\right)\right]
$$

$$
\mathcal H(\pi(\cdot\mid s))=\mathbb E_{a\sim\pi}[-\log\pi(a\mid s)]
$$

$\beta$ 是温度，即熵的权重，文献常用 $\alpha$；这里用 $\beta$ 避免与学习率混淆。连续策略中的 $\pi$ 是概率密度。

## Critic 的软目标

$$
y=r+\gamma(1-d)\left[\min_iQ_{\bar\phi_i}(s',a')-\beta\log\pi_\theta(a'\mid s')\right],\quad a'\sim\pi_\theta(\cdot\mid s')
$$

两个 Critic 仍用平方误差拟合 $y$。这里下一动作由当前随机策略采样，价值用目标 Critic 估计。

## Actor 损失

Actor 是“负责选动作的模块”，Critic 是“负责估计动作长期分数的模块”。温度 β 是权重，不是物理温度；它决定分布分散程度在目标里占多大比重。

$$
L_\pi=\mathbb E_{s\sim\mathcal D,\ a\sim\pi_\theta}\left[\beta\log\pi_\theta(a\mid s)-\min_i Q_{\phi_i}(s,a)\right]
$$

最小化损失时，既倾向高价值动作，也考虑熵项。连续实现常采用可重参数化采样，并用 tanh 压缩到动作边界；计算对数密度时要包含变换修正，不能直接使用压缩前的高斯密度。

## 算一次看看

先做熵项修正，再做折扣，最后加本步奖励。不要把本步奖励也乘上这里的折扣。

下一状态两个 Q 的较小值为 1.5，采样动作对数密度为 −0.7，$\beta=0.2$，软价值项为 $1.5-0.2\times(-0.7)=1.64$。若奖励为 −1、折扣 0.9且未终止，目标为 0.476。

## 与代码对照

`ent_coef="auto"` 让实现根据目标熵自动学习温度，不表示温度永远为 0.2。示例中的 0.2 仅为算数说明。熵奖励并不保证探索到重要状态，仍需评估实际任务成功率。

## 不看答案，自己判断一次

较小 Q 为 1.5，对数密度 −0.7，温度 0.2。软价值项是多少？

??? success "查看推理与答案"

    1.5 − 0.2 × (−0.7) = 1.64。连续动作使用密度而不是某个精确数值动作的发生概率；密度可能大于 1。

## 进一步阅读

[Spinning Up：SAC](https://spinningup.openai.com/en/latest/algorithms/sac.html)
