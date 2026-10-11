# DDPG：公式讲解

[算法直觉](../intuition/ddpg.md) · [公式讲解](ddpg.md) · [Python 实践](../code/ddpg.md)

先读 [公共符号与回报](index.md)，再看本页。所有数值例子都只用于说明一次更新。

!!! tip "先用一句人话读公式"

    Critic 目标 = 奖励 + 折扣 × 目标网络对下一动作的评分；Actor 尝试输出让当前 Critic 评分更高的动作。



!!! tip "读完这页，你应该能做到"

    区分价值误差与策略的动作梯度。

    **先会这些就够了**：Q 网络、连续动作。


## 看图梳理

![DDPG · 公式关系](../../assets/learning/rl-math-ddpg.svg){ .learning-figure }

[打开大图](../../assets/learning/rl-math-ddpg.svg)

**确定性 Actor**：输出连续动作，采样时加探索噪声；**Critic 估计 Q**：从回放池采样，目标网络构造目标；**更新与软同步**：Actor 借 Q 的梯度学习，缓慢更新目标参数。


## 更新评分器与更新动作生成器要分开

Critic 先用下一状态的目标 Actor 给出下一动作，再用目标 Critic 打分，形成奖励加未来估计。当前 Critic 通过减小预测与目标的误差学习。

Actor 的任务是生成让当前 Critic 评分更高的动作。更新 Actor 时固定 Critic 参数，但仍保留“评分随动作怎样变化”的梯度；把整个 Q 计算都断开，就没有办法把方向传给 Actor。

横线表示更新较慢的目标参数。软更新若 τ = 0.01，就是保留旧目标参数的 99%，加进新参数的 1%；它混合的是网络参数，不是每次把动作减小 1%。

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

## 不看答案，自己判断一次

Critic 预测 1.3，目标为 0.8。能否据此断言 Actor 应减小速度？

??? success "查看推理与答案"

    只能说明 Critic 当前对这个样本估得偏高。Actor 的动作改变取决于 Q 对动作的梯度，不能仅凭一个价值误差判断速度方向。

## 进一步阅读

[Spinning Up：DDPG](https://spinningup.openai.com/en/latest/algorithms/ddpg.html)
