# 第三部分：编程实践

统一使用 **Python**。基础算法直接手写，便于对照公式；深度算法使用成熟库，先建立可以运行的训练与评估闭环。每个算法都有完整代码和可下载文件。

## 两类示例

| 实现方式 | 算法 | 环境 | 依赖 |
| --- | --- | --- | --- |
| 手写更新 | 价值迭代、MC、TD、SARSA、Q-learning、REINFORCE | 一维走廊 | Python 标准库 |
| 库实现训练 | DQN、A2C、PPO | CartPole-v1 | Gymnasium、Stable-Baselines3、PyTorch |
| 库实现训练 | DDPG、TD3、SAC | Pendulum-v1 | Gymnasium、Stable-Baselines3、PyTorch |

基础脚本真的执行价值或策略更新；深度脚本真的调用训练、保存并重新加载模型。使用库实现不等于从零实现深度算法，各页会标明这一点。

## 配置独立环境

推荐 Python 3.12，将科研算法依赖与网站构建环境分开。在项目根目录运行：

```powershell
py -3.12 -m venv .venv-rl
.venv-rl/Scripts/python.exe -m pip install -r docs/rl/examples/requirements.txt
```

不使用 Windows 时，把第一行改为 `python3.12 -m venv .venv-rl`，环境解释器使用 `.venv-rl/bin/python`。

需要节省 GPU 依赖时，可以先按照 [PyTorch 官方安装说明](https://pytorch.org/get-started/locally/) 安装 CPU 版本，再安装上述依赖。脚本本身默认在 CPU 上运行，不需要 MuJoCo，也不弹出渲染窗口。

## 快速运行

基础脚本不需要安装第三方包：

```powershell
python docs/rl/examples/q-learning.py
```

深度算法使用安装好依赖的环境：

```powershell
.venv-rl/Scripts/python.exe docs/rl/examples/ppo.py --steps 10000 --seed 7
```

也可使用合并入口，方便更换算法：

```powershell
python docs/rl/examples/tabular.py sarsa
.venv-rl/Scripts/python.exe docs/rl/examples/deep_rl.py sac --steps 10000
```

如果单独下载页面里的 Python 文件，命令中的文件路径改为实际保存路径即可。

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

## 先检查运行，再判断学会没有

- 基础例子先观察价值、动作或概率是否符合环境直觉。
- 深度算法输出训练前后评估均值，以及保存的模型位置。
- 短时间运行主要检查流程，不代表收敛，也不保证回报增加。
- 正式比较需要相同环境、训练预算、评估条件和多个训练种子。

[依赖版本文件](../examples/requirements.txt) · [Gymnasium 环境接口](https://gymnasium.farama.org/api/env/) · [SB3 算法支持表](https://stable-baselines3.readthedocs.io/en/master/guide/algos.html)
