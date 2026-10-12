# 第三部分：编程实践

统一使用 **Python**。基础算法直接手写，便于对照公式；深度算法使用成熟库，通过代码认识训练与评估的数据流。每个算法都在正文中展示带注释的完整代码。

!!! tip "没学过 Python，从哪里开始？"

    先读 [Python 阅读入门](../../programming/python-reading.md)：用几行代码认识变量、列表、缩进、判断、循环与函数。再选价值迭代或 TD，一次只读一个更新步骤。无需安装 RL 环境。


## 看图梳理

![阅读 RL 代码的顺序](../../assets/learning/rl-code-index.svg){ .learning-figure }

[打开大图](../../assets/learning/rl-code-index.svg)

**背景与输入**：状态和动作的含义，基础手写或库调用；**学习步骤**：目标值或回报，找到更新语句；**检查与输出**：终止处理、独立评估，只阅读，无需 RL 环境。


## 先学会在代码里寻找四种东西

不要一口气从 import 读到最后一行。每页先给一个小片段，把某次更新中的数字写死；随后才给完整示例。小片段用于演算，不代表完整训练器。

| 先找什么 | 常见写法 | 阅读时问自己 |
| --- | --- | --- |
| 输入 | state、reward、next_state | 来自环境的事实，还是算法自己估的？ |
| 长期保存的数据 | values、q、logits、model | 多局之间保留什么才叫学到了？ |
| 临时计算 | target、error、advantage | 本条经验提供什么学习信号？ |
| 修改语句 | values[s] += … 或内部优化器 | 究竟修改哪个数、哪一组参数？ |

例如 `s = ns` 只是“把当前位置换成下一位置”，它不是学习；`q[s][a] += …` 才是在改动作评分。创建 model 也不等于训练，learn 才启动交互和参数更新。

### 两个练习环境的输入、动作各是什么

| 环境 | 看见什么 | 能做什么 | 一局怎样停下 |
| --- | --- | --- | --- |
| CartPole | 位置、速度、杆角度、杆角速度 | 动作 0 左推，1 右推 | 杆倒或小车出界是真正终止；达到外部步数上限是截断 |
| Pendulum | cos(角度)、sin(角度)、角速度 | 长度 1 的数组，给定 [−2, 2] 内的扭矩 | 标准任务主要由外部步数限制截断 |

这些接口由 [Gymnasium CartPole](https://gymnasium.farama.org/environments/classic_control/cart_pole/) 与 [Pendulum](https://gymnasium.farama.org/environments/classic_control/pendulum/) 定义。例子中的左右推或扭矩不直接等于放牧机器人速度，换研究任务时必须重新定义观测、动作和奖励。

深度算法的完整脚本还展示了保存、加载和评估。第一次只读“环境 → 创建算法 → learn”与本章独有的参数，再回来读文件处理与评估，学习主线会更清楚。

## 两类示例

| 实现方式 | 算法 | 环境 | 依赖 |
| --- | --- | --- | --- |
| 手写更新 | 价值迭代、MC、TD、SARSA、Q-learning、REINFORCE | 一维走廊 | Python 标准库 |
| 库实现训练 | DQN、A2C、PPO | CartPole-v1 | Gymnasium、Stable-Baselines3、PyTorch |
| 库实现训练 | DDPG、TD3、SAC | Pendulum-v1 | Gymnasium、Stable-Baselines3、PyTorch |

基础代码展示价值或策略怎样更新；深度代码展示训练、保存和恢复的调用顺序。使用库实现不等于从零实现深度算法，各页会标明这一点。

## 按数据流阅读，不需要运行

本部分只提供 **Python 学习代码**：不需要创建 RL 虚拟环境，也不需要安装训练依赖。网页和构建过程不会执行这些示例。

先读输入、环境和变量，再找目标值或 learn 调用，最后读输出与资源释放。中文注释解释关键变量、公式对应关系、终止处理和库负责的部分。

基础六种算法展示手写更新；深度六种算法展示库调用流程，算法内部更新请配合公式篇阅读。依赖名称用于说明代码来源，不是学习前的安装任务。

## 每个算法的代码

- [价值迭代：Python 实践](value-iteration.md)
- [蒙特卡洛（MC）：Python 实践](mc.md)
- [时序差分 TD(0)：Python 实践](td.md)
- [SARSA：Python 实践](sarsa.md)
- [Q-learning：Python 实践](q-learning.md)
- [DQN：Python 实践](dqn.md)
- [REINFORCE：Python 实践](reinforce.md)
- [Actor-Critic / A2C：Python 实践](a2c.md)
- [PPO：Python 实践](ppo.md)
- [DDPG：Python 实践](ddpg.md)
- [TD3：Python 实践](td3.md)
- [SAC：Python 实践](sac.md)

## 阅读后检查是否理解

- 基础例子用纸笔代入一次更新，检查价值、动作或概率如何改变。
- 深度例子指出哪行创建模型、哪行触发训练、哪行单独评估。
- `learn` 只是触发学习流程，不等于已经学会任务或回报必然增加。
- 正式比较需要相同环境、训练预算、评估条件和多个训练种子。

`total_timesteps` 是请求的交互步数，部分算法会收完一段数据再停止，因此实际步数可能略多。示例保留 `model.num_timesteps`，帮助区分请求预算与实际采样数量。评估只用 5 幕是为了展示接口，不足以支持可靠的算法排名；确定性评估也不代表已经检验了策略的全部随机行为。细节见 [SB3 的步数与复现说明](https://stable-baselines3.readthedocs.io/en/master/guide/algos.html)。

[Gymnasium 环境接口](https://gymnasium.farama.org/api/env/) · [SB3 算法支持表](https://stable-baselines3.readthedocs.io/en/master/guide/algos.html)
