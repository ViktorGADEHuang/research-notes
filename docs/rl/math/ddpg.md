# DDPG：公式讲解

[算法直觉](../intuition/ddpg.md) · [公式讲解](ddpg.md) · [Python 实践](../code/ddpg.md)

先读 [公共符号与回报](index.md)，再看本页。所有数值例子都只用于说明一次更新。

!!! tip "先用一句人话读公式"

    Critic 目标 = 奖励 + 折扣 × 目标网络对下一动作的评分；Actor 尝试输出让当前 Critic 评分更高的动作。


## Critic 学什么

$$
y=r+\gamma(1-d)Q_{\bar\phi}(s',\mu_{\bar\theta}(s'))
$$

$$
L_Q(\phi)=\mathbb E_{\mathcal D}[(Q_\phi(s,a)-y)^2]
$$

$\mu_\theta$ 是确定性 Actor，输入状态直接输出连续动作；横线表示目标网络。Critic 朝即时奖励加目标网络后续估计靠近。

## Actor 学什么

$$
L_\mu(\theta)=-\mathbb E_{s\sim\mathcal D}[Q_\phi(s,\mu_\theta(s))]
$$

最小化负 Q 就是提高 Q。更新 Actor 时保持 Critic 参数固定，但保留 Q 对动作的梯度，才能把“怎么改动作分数会更高”传回 Actor。

## 目标网络慢慢跟进

$$
\bar\phi\leftarrow(1-\tau)\bar\phi+\tau\phi,\qquad
\bar\theta\leftarrow(1-\tau)\bar\theta+\tau\theta
$$

$\tau$ 很小时，目标网络每次只移动一点；部分文献用 $\rho=1-\tau$，注意两种写法别混淆。

## 算一次看看

奖励 −1、折扣 0.9、下一目标 Q 为 2且未终止，目标为 0.8。当前 Q 若为 1.3，Critic 要降低它。Actor 的改动则取决于动作梯度，不能仅由这一条误差确定。

## 与代码对照

`action_noise` 用于采样探索，不属于确定性策略本身。SB3 在内部处理回放、目标网络与梯度更新。动作有上下界；这里不要把策略输出误认为某个动作被选中的概率。

## 进一步阅读

[Spinning Up：DDPG](https://spinningup.openai.com/en/latest/algorithms/ddpg.html)
