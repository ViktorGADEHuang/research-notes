# PPO：Python 实践

[算法直觉](../intuition/ppo.md) · [公式讲解](../math/ppo.md) · [Python 实践](ppo.md)


!!! tip "读完这页，你应该能做到"

    找到输入、目标或训练调用，再对照公式解释关键注释。

    **先会这些就够了**：优势、新旧策略；本页讲 PPO-Clip。


## 看图梳理

![PPO · 代码数据流](../../assets/learning/rl-code-ppo.svg){ .learning-figure }

[打开大图](../../assets/learning/rl-code-ppo.svg)

**先用旧策略采样**：保留旧 log 概率，估计优势；**比较新旧概率**：概率比率乘优势，裁剪目标的优化激励；**有限次数更新**：对一批数据多轮优化，裁剪不是概率硬限制。


还不认识 Python 的列表、循环或缩进？先查 [Python 阅读入门](../../programming/python-reading.md)，再回来读本页。

## 示例背景

**语言：Python 3.12；实现方式：使用 Stable-Baselines3 的真实算法实现。**

本页先学习如何调用算法、训练、保存与评估。网络结构与梯度更新由库实现。完整脚本用于阅读训练、保存与评估的调用顺序，内部算法细节要与前两部分对照。


本页以阅读代码为主，不要求安装依赖或运行训练。

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

## 把三个采样配置分别对应到工作节奏

示例一个环境，n_steps = 256：先收集 256 步。batch_size = 64：更新时把采样数据分成小批。n_epochs = 4：对同一批数据做四轮训练。不要把四轮训练误读成只在环境里走四步。

每轮小批使用采样时保存的旧动作概率，与当前新概率比较，再配合优势形成目标。新的数据收集开始后，新一批才有自己的旧策略基准。

`clip_range = 0.2` 对应围绕 1 的 0.8～1.2 比率范围，不是动作取值范围，也不是 20% 的随机探索概率。下面库负责这套内部更新，阅读时先找到三个节奏参数和裁剪参数。

## 用八行数字代码看清裁剪发生在哪里

```python
# 只比较同一状态、同一采样动作；旧概率在本批所有更新中不变。
old_probability, new_probability = 0.2, 0.3
advantage, clip_range = 2.0, 0.2
ratio = new_probability / old_probability  # 1.5。
clipped_ratio = min(max(ratio, 1 - clip_range), 1 + clip_range)  # 1.2。
original_term = ratio * advantage          # 3.0。
clipped_term = clipped_ratio * advantage   # 2.4。
objective = min(original_term, clipped_term)  # 2.4，要提高的目标。
policy_loss = -objective                     # -2.4，优化器要减小的损失。
# new_probability 仍是 0.3，上面的运算没有给它重新赋值。
```

把 advantage 换成 −2、把 new_probability 换成 0.1，便得到原项 −1、裁剪项 −1.6，min 为 −1.6。负数也照常按大小比较。损失可以为负；优化器关心它怎样随参数变化，不要求损失一定从正数降到 0。

| 完整代码配置或数据 | 本例数值 | 应该怎样读 |
| --- | --- | --- |
| `n_steps` | 256 | 单环境收集 256 条记录 |
| `batch_size` | 64 | 每次拿 64 条记录更新 |
| `n_epochs` | 4 | 同一批数据遍历 4 轮，通常共 16 次小批更新 |
| 旧 log 概率、优势 | 每条记录各一个 | 与观测、动作对应，不能把记录顺序弄乱 |

16 来自 `256 ÷ 64 × 4`，是本例无提前停止、批次整除时的学习次数。它不是又与环境交互了 16 步。完整网络还学习状态价值；上面的短片段只展示策略损失中的裁剪项。

## 完整代码

```python title="ppo · 完整学习代码"
"""PPO 训练、保存与独立评估；默认 10000 步，可传 --steps 调整。"""
# 命令行参数工具；阅读算法时可先跳过参数解析部分。
import argparse
from pathlib import Path
# 环境接口库：提供 reset 开始一局、step 执行动作。
import gymnasium as gym
# 神经网络库；本示例的网络与梯度计算由 SB3 调用它完成。
import torch
# 导入库实现的算法；调用库并不等于从零实现算法内部。
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.evaluation import evaluate_policy


def main(steps, seed):
    # 限制 CPU 计算线程数量，不代表启动机器人或仿真控制线程。
    torch.set_num_threads(1)
    # Path 表示文件路径；后面的 / 是拼接子路径，并非这里在做数字除法。
    output = Path("rl-output/ppo")
    # 只有主动运行脚本才创建输出目录；网站展示代码不会执行这一行。
    output.mkdir(parents=True, exist_ok=True)
    # 训练环境负责收集经验，Monitor 统计每幕奖励与步数。
    train_env = Monitor(gym.make("CartPole-v1"), str(output / "train"))
    # 另建评估环境，避免把训练过程中的奖励直接当作评估结果。
    eval_env = Monitor(gym.make("CartPole-v1"))
    # 评估随机种子单独设置；它不保证跨硬件逐位一致。
    # reset 返回初始观测和 info；评估器之后会自行按回合调用环境接口。
    eval_env.reset(seed=seed + 100)
    try:
        # 创建策略与价值网络；初始化完成不意味着模型已经学会任务。
        model = PPO(
            # 多层感知机策略；seed 控制随机初始化，device 指定 CPU。
            "MlpPolicy", train_env, seed=seed, device="cpu", verbose=0,
            # 采集长度决定一次更新前收集多少步；PPO 还会分小批量重复更新。
            n_steps=256, batch_size=64, n_epochs=4, clip_range=0.2,
        )
        # 记录未训练策略的评估均值，作为观察起点。
        # 左边两个名字接收均值和标准差；这里用 _ 表示暂时不使用第二项。
        before, _ = evaluate_policy(model, eval_env, n_eval_episodes=5,
                                   deterministic=True)
        # 这行才触发训练；本教程只提供代码，不在项目中自动调用。
        model.learn(total_timesteps=steps)
        # 保存参数，便于理解模型持久化，不表示策略性能已达标。
        model.save(str(output / "model"))
        # 从磁盘重新加载模型，展示部署前参数恢复的步骤。
        loaded = PPO.load(str(output / "model"), device="cpu")
        # 评估随机种子单独设置；它不保证跨硬件逐位一致。
        eval_env.reset(seed=seed + 100)
        # 使用独立环境评估恢复的模型，输出平均回报与标准差。
        # std 是这些评估回合回报的标准差，不是训练结果可靠性的保证。
        after, std = evaluate_policy(loaded, eval_env, n_eval_episodes=5,
                                    deterministic=True)
        print(f"Actual training steps: {model.num_timesteps}")
        print(f"Before: {before:.2f} | After: {after:.2f} +/- {std:.2f}")
        print(f"Model saved to: {output / 'model.zip'}")
    # 即使中间发生异常，也尝试释放环境资源。
    finally:
        train_env.close()
        eval_env.close()


# 入口保护：被导入时不调用这里的 main；网站只展示文本。
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    # steps 是训练预算示例，不是预期学会任务所需的精确步数。
    parser.add_argument("--steps", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=7)
    # 把可选命令行文字转换为参数值；定义参数本身不会启动学习。
    args = parser.parse_args()
    if args.steps <= 0:
        parser.error("--steps must be positive")
    main(args.steps, args.seed)
```

## 参数如何对应算法

`n_steps` 对应一轮采样长度；`n_epochs` 是对同批数据更新的轮数；`clip_range` 是概率比裁剪阈值。

`MlpPolicy` 是多层感知机策略，用于向量观测；如果改为图像或字典观测，需要选择相应策略与输入处理。脚本设置独立评估环境，使用固定的一组评估起始条件，并保存训练日志与模型。

## 看懂输出

- `Actual training steps`：实际交互步数。同策略方法可能为凑齐完整 rollout 超过请求步数。
- `Before`：未训练模型的确定性评估均值。
- `After`：保存并重新加载模型后，5 幕独立评估的均值与标准差。
- `rl-output/ppo/model.zip`：模型文件；同目录的 `train.monitor.csv` 保存训练回合记录。

运行成功只说明接口与训练链路正常。判断学习效果还需要更充分的训练、更多评估回合和多个训练种子。

## 阅读练习：把理解分成三小步

<div class="practice-card" markdown="1">

<p class="practice-kicker">纸笔演算，不需要运行训练</p>

<p class="practice-title">四行数值对照，不只看是否超界</p>

**沿用这些条件**：裁剪阈值 0.2；分别考虑正优势 2 与负优势 −2，比率各取 1.5 和 0.5。

**从哪里开始**：回到本页的核心短片段，先圈出输入和旧预测，再计算临时目标；最后才判断要修改什么。

**按这几步做**：

1. 列出四种组合的原项与裁剪项。
2. 每种组合按数值取 min。
3. 解释比率超界时是否总用裁剪项，原动作概率是否被这段算术改写。

??? tip "先要一点提示？"

    给每个数写上名字，区分奖励、旧预测、目标、参数或动作。每算完一步，把中间结果写下来，再进入下一步，不只抄最后答案。

??? example "对照完整推理"

    优势 2、比率 1.5：原项 3，裁剪项 2.4，取 2.4；优势 2、比率 0.5：原项 1，裁剪项 1.6，取 1。优势 −2、比率 0.5：原项 −1，裁剪项 −1.6，取 −1.6；优势 −2、比率 1.5：原项 −3，裁剪项 −2.4，取 −3。

    因此超界也可能保留原项，取决于优势符号与 min。这个片段只构造目标值，没有给原概率重新赋值。参数更新由完整损失、整批样本与优化器共同决定。

</div>


## 官方实现说明

[Stable-Baselines3：PPO](https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html)
