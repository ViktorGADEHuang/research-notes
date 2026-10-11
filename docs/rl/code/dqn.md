# DQN：Python 实践

[算法直觉](../intuition/dqn.md) · [公式讲解](../math/dqn.md) · [Python 实践](dqn.md)

## 环境与依赖

**语言：Python 3.12；实现方式：使用 Stable-Baselines3 的真实算法实现。**

本页先学习如何调用算法、训练、保存与评估。网络结构与梯度更新由库实现，完整脚本可运行，但它不是从零手写算法。

安装依赖的步骤见 [编程实践首页](index.md)。从项目根目录执行：

```bash
python -m pip install -r docs/rl/examples/requirements.txt
python docs/rl/examples/dqn.py --steps 10000
```

或者 [下载完整 Python 文件](../examples/dqn.py){ .md-button } 后，在所在目录运行 `python dqn.py --steps 10000`。

## 示例任务

**CartPole-v1**：左右推动小车，让杆保持直立；动作是离散的，回报越高表示维持时间越长。

这是训练链路示例，不是放牧仿真，也不保证使用默认 10000 步就解决环境。

## 用中文顺着读代码

1. `gym.make(...)`：创建一个用来练习的环境。
2. `Monitor(...)`：记录每局拿了多少奖励、走了多少步。
3. 创建模型：选算法和它的配置，模型此时还没学会任务。
4. 第一次 `evaluate_policy(...)`：测一下未训练时的表现。
5. `model.learn(...)`：真正与环境交互，并更新网络。
6. `save` 与 `load`：把学到的参数保存，再从文件读回来。
7. 再次评估：使用独立环境检查保存后的策略表现。

环境的 `reset` 是开始新一局；`step` 是执行一次动作。这里库负责调用它们。`seed` 固定随机数起点，便于复现；它不意味着不同硬件一定得到完全相同的结果。

## 完整代码

```python
"""DQN 训练、保存与独立评估；默认 10000 步，可传 --steps 调整。"""
import argparse
from pathlib import Path
import gymnasium as gym
import numpy as np
import torch
from stable_baselines3 import DQN
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.evaluation import evaluate_policy


def main(steps, seed):
    torch.set_num_threads(1)
    output = Path("rl-output/dqn")
    output.mkdir(parents=True, exist_ok=True)
    train_env = Monitor(gym.make("CartPole-v1"), str(output / "train"))
    eval_env = Monitor(gym.make("CartPole-v1"))
    eval_env.reset(seed=seed + 100)
    try:
        model = DQN(
            "MlpPolicy", train_env, seed=seed, device="cpu", verbose=0,
            buffer_size=20000, learning_starts=100, batch_size=64,
        train_freq=1, gradient_steps=1, target_update_interval=250,
        exploration_fraction=0.3,
        )
        before, _ = evaluate_policy(model, eval_env, n_eval_episodes=5,
                                   deterministic=True)
        model.learn(total_timesteps=steps)
        model.save(str(output / "model"))
        loaded = DQN.load(str(output / "model"), device="cpu")
        eval_env.reset(seed=seed + 100)
        after, std = evaluate_policy(loaded, eval_env, n_eval_episodes=5,
                                    deterministic=True)
        print(f"Actual training steps: {model.num_timesteps}")
        print(f"Before: {before:.2f} | After: {after:.2f} +/- {std:.2f}")
        print(f"Model saved to: {output / 'model.zip'}")
    finally:
        train_env.close()
        eval_env.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--steps", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()
    if args.steps <= 0:
        parser.error("--steps must be positive")
    main(args.steps, args.seed)
```

## 参数如何对应算法

`buffer_size` 是经验池容量；`learning_starts` 是开始更新前的采样步数；`target_update_interval` 是目标网络同步间隔；探索设置控制随机动作比例的变化。

`MlpPolicy` 是多层感知机策略，用于向量观测；如果改为图像或字典观测，需要选择相应策略与输入处理。脚本设置独立评估环境，使用固定的一组评估起始条件，并保存训练日志与模型。

## 看懂输出

- `Actual training steps`：实际交互步数。同策略方法可能为凑齐完整 rollout 超过请求步数。
- `Before`：未训练模型的确定性评估均值。
- `After`：保存并重新加载模型后，5 幕独立评估的均值与标准差。
- `rl-output/dqn/model.zip`：模型文件；同目录的 `train.monitor.csv` 保存训练回合记录。

运行成功只说明接口与训练链路正常。判断学习效果还需要更充分的训练、更多评估回合和多个训练种子。

## 动手修改

观察训练步数变多时，评估回报是否提升，再改变目标同步间隔。

若要连接放牧任务，先实现并检查自己的 Gymnasium 环境，再替换 `gym.make` 创建的环境。保持动作空间、奖励定义与终止条件明确，不直接套用本页的超参数作为科研结论。

## 官方实现说明

[Stable-Baselines3：DQN](https://stable-baselines3.readthedocs.io/en/master/modules/dqn.html)
