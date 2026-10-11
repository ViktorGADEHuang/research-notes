# SAC：公式讲解

[算法直觉](../intuition/sac.md) · [公式讲解](sac.md) · [Python 实践](../code/sac.md)

先读 [公共符号与回报](index.md)，再看本页。所有数值例子都只用于说明一次更新。

!!! tip "先用一句人话读公式"

    Critic 学习“奖励 + 折扣后的未来评分与熵”；Actor 同时追求高 Q 与策略熵；温度决定两者怎么权衡。


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

$$
L_\pi=\mathbb E_{s\sim\mathcal D,\ a\sim\pi_\theta}\left[\beta\log\pi_\theta(a\mid s)-\min_i Q_{\phi_i}(s,a)\right]
$$

最小化损失时，既倾向高价值动作，也考虑熵项。连续实现常采用可重参数化采样，并用 tanh 压缩到动作边界；计算对数密度时要包含变换修正，不能直接使用压缩前的高斯密度。

## 算一次看看

下一状态两个 Q 的较小值为 1.5，采样动作对数密度为 −0.7，$\beta=0.2$，软价值项为 $1.5-0.2\times(-0.7)=1.64$。若奖励为 −1、折扣 0.9且未终止，目标为 0.476。

## 与代码对照

`ent_coef="auto"` 让实现根据目标熵自动学习温度，不表示温度永远为 0.2。示例中的 0.2 仅为算数说明。熵奖励并不保证探索到重要状态，仍需评估实际任务成功率。

## 进一步阅读

[Spinning Up：SAC](https://spinningup.openai.com/en/latest/algorithms/sac.html)
