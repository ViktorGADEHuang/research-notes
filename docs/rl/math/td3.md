# TD3：公式讲解

[算法直觉](../intuition/td3.md) · [公式讲解](td3.md) · [Python 实践](../code/td3.md)

先读 [公共符号与回报](index.md)，再看本页。所有数值例子都只用于说明一次更新。

!!! tip "先用一句人话读公式"

    先给目标动作加有界小噪声；两个目标 Q 取小，算 Critic 目标；Actor 隔若干次更新一次。


先记住：$\mu_\theta(s)$ 是 Actor 输出的确定性动作，$Q_{\phi_i}$ 是第 $i$ 个 Critic，横线表示目标网络参数。$\sigma$ 是目标噪声的标准差，$I$ 是单位矩阵，表示各动作维度使用独立同尺度的高斯噪声。

## 平滑目标动作

$$
\tilde a'=\operatorname{clip}(\mu_{\bar\theta}(s')+\operatorname{clip}(\xi,-c,c),a_{\min},a_{\max}),\quad \xi\sim\mathcal N(0,\sigma^2 I)
$$

$\xi$ 是高斯小噪声，$c$ 限制它的幅度，外层裁剪保证动作不超界。它用于训练目标，与环境采样时的探索噪声不同。

## 双 Q 目标

$$
y=r+\gamma(1-d)\min_{i\in\{1,2\}}Q_{\bar\phi_i}(s',\tilde a')
$$

$$
L_{Q_i}=\mathbb E_{\mathcal D}[(Q_{\phi_i}(s,a)-y)^2],\qquad
L_\mu=-\mathbb E_{\mathcal D}[Q_{\phi_1}(s,\mu_\theta(s))]
$$

两个 Critic 都追同一个保守目标，Actor 通常使用第一个 Critic 提供的梯度。双 Q 取小发生在目标中，不是每个地方都必须取小。

## 算一次看看

两个目标 Q 分别为 2.4、1.8，奖励为 0.1、折扣 0.9且未终止，目标为 $0.1+0.9\times1.8=1.72$。只用较高估计会得到 2.26，可能更容易把乐观误差传下去。

## 延迟更新

每次训练可以更新 Critic，而 Actor 与目标网络隔若干次再更新。这里的“延迟”指梯度更新节奏，不是故意让机器人晚执行动作。

## 与代码对照

SB3 的 `policy_delay` 控制策略更新间隔，`target_policy_noise` 和 `target_noise_clip` 控制目标平滑。示例另外配置的 `action_noise` 是交互探索噪声。Actor 与 Critic 的软更新方式沿用 DDPG 思路。

## 进一步阅读

[Spinning Up：TD3](https://spinningup.openai.com/en/latest/algorithms/td3.html)
