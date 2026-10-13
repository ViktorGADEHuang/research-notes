# DQN：Python 实践

[算法直觉](../intuition/dqn.md) · [公式讲解](../math/dqn.md) · [Python 实践](dqn.md)


!!! tip "读完这页，你应该能做到"

    从一条转移算出 TD 目标与平滑 L1 损失，再指出库在哪一步训练 Q 网络。

    **先会这些就够了**：Q-learning、平方误差。

## 看图梳理

![DQN · 代码数据流](../../assets/learning/rl-code-dqn.svg){ .learning-figure }

[打开大图](../../assets/learning/rl-code-dqn.svg)

**收集与存经验**：状态、动作、奖励，经验回放池；**构造稳定目标**：目标网络估计最大 Q，终止时屏蔽后续项；**训练 Q 网络**：减小预测与目标差，梯度与同步由库实现。


还不认识 Python 的列表、循环或缩进？先查 [Python 阅读入门](../../programming/python-reading.md)，再回来读本页。

## 示例背景

**语言：Python 3.12；实现方式：使用 Stable-Baselines3 的真实算法实现。**

本页先学习如何调用算法、训练、保存与评估。网络结构与梯度更新由库实现。完整脚本用于阅读训练、保存与评估的调用顺序，内部算法细节要与前两部分对照。


本页以阅读代码为主，不要求安装依赖或运行训练。

## 示例任务

**CartPole-v1**：左右推动小车，让杆保持直立；动作是离散的，回报越高表示维持时间越长。

这是库调用流程示例，不是放牧仿真。完整脚本的折扣固定为 0.99，默认请求 10000 个环境步；短片段的折扣另行给定用于演算，不能直接当作库日志。

## 库调用藏起了哪些内部步骤

`DQN(...)` 创建网络、回放池与配置；它不会立刻给出学会的策略。`model.learn(...)` 内部重复“选动作 → 交互 → 存记录 → 抽样 → 算目标 → 改网络”。网页上的调用行短，背后的过程并不只有一行。

| 配置 | 可以先理解为 |
| --- | --- |
| buffer_size = 20000 | 最多保存多少条转移记录 |
| learning_starts = 100 | 先收集一些记录再开始梯度学习 |
| batch_size = 64 | 一次拿多少条记录构成训练批次 |
| target_update_interval = 250 | 按采样步数定期同步目标网络 |

本例探索率在前 30% 请求步数内由 1 降到 0.05，此后保持 0.05。探索表示随机选动作；随机选时仍可能选到最高分动作。先读配置的用途，不要把这些教学数字当成最优参数。单条记录中下一状态的最高分如何进入目标，回到公式篇的算例理解；这里只展示库的使用流程。

## 先读一条样本的学习过程

下面用普通数字展开 DQN 的一条训练样本。它不包含网络和优化器，只用于把公式与 Python 运算对应起来。

```python
# 实际执行动作之后，获得奖励 1，且环境尚未真正终止。
reward, gamma, terminated = 1.0, 0.9, False
next_q_from_target = [1.0, 2.0]  # 目标网络对下一状态两个动作的预测。
future = 0.0 if terminated else gamma * max(next_q_from_target)
target = reward + future         # 2.8，计算这一目标时不回传梯度。
predicted_q = 1.4                # 当前网络对刚执行动作的 Q 预测。
error = predicted_q - target     # -1.4，提示当前预测偏低。
absolute_error = abs(error)
# SB3 使用平滑 L1 损失：误差绝对值小于 1 时用二次段，否则用线性段。
loss = 0.5 * error**2 if absolute_error < 1 else absolute_error - 0.5
# 这条样本的损失为 0.9；一批样本求平均后才进行网络梯度更新。
```

之后看完整代码中的 `model.learn`，就把它展开读成“反复采样、抽回放数据、计算上面这种目标、用梯度改 Q 网络”。它还负责终止与外部截断的处理，不能自行把两者都当作未来价值为零。

| 数据 | 本示例大小 | 内容 |
| --- | --- | --- |
| 单条观测 | 4 个数 | 小车位置、速度、杆角度、杆角速度 |
| Q 网络单条输出 | 2 个数 | 左推、右推的长期分数 |
| 实际动作 | 1 个整数 | 0 或 1 |
| 一批观测 | 64×4 | batch_size=64；不是 64 个动作 |
| 当前被选动作的 Q | 每条一个，合计 64 个 | 用记录中的动作编号从网络输出里取出 |

上述输入、动作含义对应 [CartPole 环境说明](https://gymnasium.farama.org/environments/classic_control/cart_pole/)。DQN 没有 A2C 那样单独的 Actor；SB3 虽使用通用名称 MlpPolicy，这里实际用 Q 分数来选动作。

## 看懂输出

- `Actual training steps`：实际交互步数；本例单环境、逐步采样，不需要凑齐 A2C/PPO 的固定长度片段。
- `Before`：未训练模型的确定性评估均值。
- `After`：保存并重新加载模型后，5 幕独立评估的均值与标准差。
- `rl-output/dqn/model.zip`：模型文件；同目录的 `train.monitor.csv` 保存训练回合记录。

运行成功只说明接口与训练链路正常。判断学习效果还需要更充分的训练、更多评估回合和多个训练种子。

## 阅读练习：把理解分成三小步

<div class="practice-card" markdown="1">

<p class="practice-kicker">纸笔演算，不需要运行训练</p>

<p class="practice-title">从一条转移读懂目标与损失</p>

**沿用这些条件**：未终止，奖励 1、折扣 0.9，目标网络下一 Q=[1, 2]；当前网络对实际动作预测 1.4。

**从哪里开始**：回到本页的核心短片段，先圈出输入和旧预测，再计算临时目标；最后才判断要修改什么。

**按这几步做**：

1. 算 TD 目标、误差和平方损失示意。
2. 按本页平滑 L1 片段算实际示意损失。
3. 若改为真正终止，目标如何变化？应该训练哪个网络？

??? tip "先要一点提示？"

    给每个数写上名字，区分奖励、旧预测、目标、参数或动作。每算完一步，把中间结果写下来，再进入下一步，不只抄最后答案。

??? example "对照完整推理"

    目标为 1+0.9×2=2.8；预测减目标为 −1.4；平方损失为 1.96。平滑 L1 处在线性段，得到 |−1.4|−0.5=0.9。两种损失的数字不同，不能把 1.96 当成库必定显示的结果。

    真正终止时目标只为即时奖励 1，不再使用下一状态 Q；此时误差为 0.4。训练当前网络去拟合固定目标，目标网络按同步安排跟进；不能通过同时自由改变参考目标来消除这条误差。

</div>

## 第二遍再读完整脚本

先用上面的短片段和练习弄清更新目标，再展开脚本追踪“创建模型 → 训练 → 保存 → 重新加载 → 独立评估”。保存文件与命令行参数不参与算法公式。

??? note "展开带注释的完整脚本"

    ```python title="dqn · 完整学习代码"
    """DQN 训练、保存与独立评估；默认 10000 步，可传 --steps 调整。"""
    # 命令行参数工具；阅读算法时可先跳过参数解析部分。
    import argparse
    from pathlib import Path
    # 环境接口库：提供 reset 开始一局、step 执行动作。
    import gymnasium as gym
    # 神经网络库；本示例的网络与梯度计算由 SB3 调用它完成。
    import torch
    # 导入库实现的算法；调用库并不等于从零实现算法内部。
    from stable_baselines3 import DQN
    from stable_baselines3.common.monitor import Monitor
    from stable_baselines3.common.evaluation import evaluate_policy


    def main(steps, seed):
        # 限制 CPU 计算线程数量，不代表启动机器人或仿真控制线程。
        torch.set_num_threads(1)
        # Path 表示文件路径；后面的 / 是拼接子路径，并非这里在做数字除法。
        output = Path("rl-output/dqn")
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
            # 建立当前 Q 网络与目标 Q 网络；本算法按动作分数决策，没有另一个 Actor。
            model = DQN(
                # 多层感知机策略；seed 控制随机初始化，device 指定 CPU。
                "MlpPolicy", train_env, seed=seed, device="cpu", verbose=0,
                # 完整示例折扣固定为 0.99；正文短算例另给折扣，便于口算。
                gamma=0.99,
                # 经验回放容量、开始学习前的采样步数、每批样本数。
                buffer_size=20000, learning_starts=100, batch_size=64,
                # 每交互一步后进行一次梯度更新；训练初期先积累经验。
                train_freq=1, gradient_steps=1, target_update_interval=250,
                # 前 30% 请求步数内，探索率由 1 降至 0.05；随后保持 0.05。
                exploration_fraction=0.3,
                exploration_initial_eps=1.0, exploration_final_eps=0.05,
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
            loaded = DQN.load(str(output / "model"), device="cpu")
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

## 官方实现说明

[Stable-Baselines3：DQN](https://stable-baselines3.readthedocs.io/en/v2.9.0/modules/dqn.html)
