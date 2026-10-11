# 强化学习

强化学习是在与环境交互中学习决策：观察当前情况，尝试动作，收到奖励，再调整下一次的选择。

本栏目按 **算法直觉 → 公式讲解 → 编程实践** 组织。三个部分覆盖同一组算法，可以顺着读，也可以直接查某个算法。

<div class="grid cards rl-sections" markdown="1">

-   **01 · 算法直觉**

    先用走廊、决策与反馈的例子，理解算法解决什么问题、怎样学习以及有什么限制。

    [从通俗解释开始 →](intuition/index.md)

-   **02 · 公式讲解**

    每个符号都有解释，每个核心更新都有数字例子，并说明目标与损失的区别。

    [读懂公式 →](math/index.md)

-   **03 · 编程实践**

    用 Python 动手实现基础更新，再运行深度算法的训练、保存与独立评估。

    [运行代码 →](code/index.md)

</div>


## 看图梳理

![强化学习的三条学习线](../assets/learning/rl-index.svg){ .learning-figure }

[打开大图](../assets/learning/rl-index.svg)

**算法直觉**：它解决什么问题，一轮学习做什么；**公式理解**：每个符号是什么意思，代入一次具体数值；**阅读代码**：输入、目标、更新，对照注释，不要求运行。


## 算法索引

先覆盖以下 12 类经典方法。强化学习还包含其他算法与扩展，这张表是本栏目的学习范围。

| 算法 | 通俗解释 | 公式讲解 | 编程实践 |
| --- | --- | --- | --- |
| 价值迭代 | [根据已知规则反复计算每一步的长期价值。](intuition/value-iteration.md) | [公式](math/value-iteration.md) | [Python](code/value-iteration.md) |
| 蒙特卡洛（MC） | [先走完整条路，再用真实回报给经过的状态打分。](intuition/mc.md) | [公式](math/mc.md) | [Python](code/mc.md) |
| 时序差分 TD(0) | [走一步就更新：眼前奖励加上对下一步的估计。](intuition/td.md) | [公式](math/td.md) | [Python](code/td.md) |
| SARSA | [按实际下一步会选的动作，更新当前动作的价值。](intuition/sarsa.md) | [公式](math/sarsa.md) | [Python](code/sarsa.md) |
| Q-learning | [按下一步最好的估计，更新当前动作的价值。](intuition/q-learning.md) | [公式](math/q-learning.md) | [Python](code/q-learning.md) |
| DQN | [用神经网络代替 Q 表，学习每个动作的分数。](intuition/dqn.md) | [公式](math/dqn.md) | [Python](code/dqn.md) |
| REINFORCE | [提高带来好回报的动作概率，直接学习决策规则。](intuition/reinforce.md) | [公式](math/reinforce.md) | [Python](code/reinforce.md) |
| Actor-Critic / A2C | [一个模块做决定，另一个模块评估决定好不好。](intuition/a2c.md) | [公式](math/a2c.md) | [Python](code/a2c.md) |
| PPO | [改进策略时克制一点，避免一次更新改变太大。](intuition/ppo.md) | [公式](math/ppo.md) | [Python](code/ppo.md) |
| DDPG | [直接给出连续动作，用价值网络指导动作改进。](intuition/ddpg.md) | [公式](math/ddpg.md) | [Python](code/ddpg.md) |
| TD3 | [用双重价值估计、延迟更新与目标平滑改进 DDPG。](intuition/td3.md) | [公式](math/td3.md) | [Python](code/td3.md) |
| SAC | [兼顾回报与探索，学习带随机性的连续控制策略。](intuition/sac.md) | [公式](math/sac.md) | [Python](code/sac.md) |

## 建议学习顺序

1. **建立概念**：状态、动作、奖励、回报、策略与价值。
2. **理解价值更新**：价值迭代 → MC → TD(0)。其中 MC 与 TD 的示例先评估固定策略。
3. **学会选动作**：SARSA → Q-learning → DQN。
4. **直接学策略**：REINFORCE → Actor-Critic / A2C → PPO。
5. **理解连续控制**：DDPG → TD3 → SAC。

## 和放牧机器人研究的关系

目前研究方向是放牧机器人，强化学习是相关技术学习的一部分。离散的高层动作与连续的速度指令适用的方法不同；先明确任务和动作空间，再选候选算法做对照实验。本栏目代码先使用小环境学习算法，不宣称已完成放牧实验。
