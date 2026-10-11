# REINFORCE：公式讲解

[算法直觉](../intuition/reinforce.md) · [公式讲解](reinforce.md) · [Python 实践](../code/reinforce.md)

先读 [公共符号与回报](index.md)，再看本页。所有数值例子都只用于说明一次更新。

!!! tip "先用一句人话读公式"

    参数改变量 = 学习率 × 各时刻的折扣权重 × 回报 × 提高采样动作概率的梯度，最后把各时刻贡献相加。



!!! tip "读完这页，你应该能做到"

    看懂回报怎样给动作概率的梯度加权。

    **先会这些就够了**：概率、回报；梯度可以先按“变化方向”理解。


## 看图梳理

![REINFORCE · 公式关系](../../assets/learning/rl-math-reinforce.svg){ .learning-figure }

[打开大图](../../assets/learning/rl-math-reinforce.svg)

**按当前策略采样**：概率分布选择动作，记录完整一幕；**计算回报与梯度**：折扣奖励得到 G，G 乘 log 概率梯度；**整体更新策略**：先在旧参数算梯度，再执行梯度上升。


## 目标与更新

考虑折扣的起点回报目标 $J(\theta)=\mathbb E[G_0]$，其一幕采样的更新估计为：

$$
\theta\leftarrow\theta+\eta\sum_{t=0}^{T-1}\gamma^tG_t\nabla_\theta\log\pi_\theta(a_t\mid s_t)
$$

## 逐项读懂

- $\theta$：策略参数；$\eta$：策略学习率。
- $\pi_\theta(a\mid s)$：该状态选择动作的概率。
- $\log\pi$ 的梯度：指示如何改变参数来提高采样动作的概率。
- $G_t$：从这一步开始的真实折扣回报。
- $\gamma^t$：对于这里定义的折扣起点目标，对时刻 $t$ 的贡献再加权。很多实现采用不同的采样目标或近似写法而省略该项；本篇公式与代码保留它。

## softmax 怎么变成代码

$$
\pi(a\mid s)=\frac{e^{z_{s,a}}}{\sum_j e^{z_{s,j}}},\qquad
\frac{\partial\log\pi(a\mid s)}{\partial z_{s,j}}=\mathbf1[j=a]-\pi(j\mid s)
$$

$z$ 是每个动作的可学习偏好。若动作概率为 0.4，选择了该动作，它自己的梯度项为 0.6；另一个概率为 0.6 的动作梯度项为 −0.6。

## 算一次看看

在第一步，$G_0=1$、$\eta=0.02$，选中动作的偏好增量为 0.012，另一动作减 0.012。softmax 重新计算后，选中动作的概率上升。

## 与代码对照

`logits` 对应 $z$；`gradients` 累积一幕的梯度，在采样策略参数不变的情况下计算完，再整体更新。若边回溯边改参数，再用改后的概率算前面的梯度，就不再是同一旧策略上的梯度估计。

## 不看答案，自己判断一次

选中动作的概率为 0.4，它的 log 概率对自身偏好的梯度项是多少？如果回报为负，权重方向怎样变？

??? success "查看推理与答案"

    梯度项为 1 − 0.4 = 0.6。负回报乘上它得到负方向，在这个无基线示例中倾向降低该动作偏好；不要把无基线的正负回报与优势混为一谈。

## 进一步阅读

[Spinning Up：策略梯度](https://spinningup.openai.com/en/latest/algorithms/vpg.html)

[David Silver 对应课程讲义](https://davidstarsilver.wordpress.com/wp-content/uploads/2025/04/lecture-7-policy-gradient-methods.pdf)
