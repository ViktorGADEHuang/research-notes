# SAC：Python 实践

[算法直觉](../intuition/sac.md) · [公式讲解](../math/sac.md) · [Python 实践](sac.md)


!!! tip "读完这页，你应该能做到"

    算出带熵项的 Critic 目标，说明随机动作、对数密度和自动温度各负责什么。

    **先会这些就够了**：双 Q、随机策略；熵可先按“分布的分散程度”理解。

## 看图梳理

![SAC · 代码数据流](../../assets/learning/rl-code-sac.svg){ .learning-figure }

[打开大图](../../assets/learning/rl-code-sac.svg)

**随机策略采样**：连续动作概率密度，经验回放；**奖励与熵目标**：兼顾回报和探索，双 Q 帮助减少偏差；**更新策略与价值**：Actor、Critic 分别优化，auto 可调熵温度。


还不认识 Python 的列表、循环或缩进？先查 [Python 阅读入门](../../programming/python-reading.md)，再回来读本页。

## 示例背景

**语言：Python 3.12；实现方式：使用 Stable-Baselines3 的真实算法实现。**

本页先学习如何调用算法、训练、保存与评估。网络结构与梯度更新由库实现。完整脚本用于阅读训练、保存与评估的调用顺序，内部算法细节要与前两部分对照。


本页以阅读代码为主，不要求安装依赖或运行训练。

## 示例任务

**Pendulum-v1**：对摆杆施加连续扭矩，使其接近直立；奖励通常为负，数值越接近 0 越好。

这是库调用流程示例，不是放牧仿真。完整脚本的折扣固定为 0.99，默认请求 10000 个环境步；短片段的折扣另行给定用于演算，不能直接当作库日志。

## 随机训练策略，为什么评估却写 deterministic

训练时策略分布用来采样动作，并计算密度参与熵目标。示例调用 `evaluate_policy(..., deterministic=True)`，使用库定义的确定性预测动作，便于展示一种评估方式；这不会把训练算法改成 DDPG。

`ent_coef = "auto"` 让库学习熵系数。它不是 Python 自动猜一个最佳算法，也不是把所有探索参数都自动解决。回放批次和网络仍受其他配置影响。

SAC 的随机策略本身提供探索，本例没有配置 DDPG/TD3 那种 action_noise。先看创建模型的差异，再对照公式找温度项。5 幕评估只展示接口，还不能支持算法优劣结论。

## 把带熵的目标翻译成几行 Python

```python
# 下一动作由当前随机策略采样，两个目标 Critic 给它评分。
next_q1, next_q2 = 1.8, 1.5
next_log_density = -0.7  # 已包含动作变换修正后的对数密度，假想数值。
temperature = 0.2       # 本段固定用 0.2 演算；完整代码使用 auto 学温度。
soft_future = min(next_q1, next_q2) - temperature * next_log_density  # 1.64。
reward, gamma, terminated = -1.0, 0.9, False
target = reward + (0.0 if terminated else gamma * soft_future)  # 0.476。
# 真正终止时，不把后续 Q 或后续熵加进目标；target 只剩 reward。
```

这里没有从概率中减掉熵，改的是用于学习的目标。next_log_density 对应刚才采样的**那个下一动作**，不能随便换另一个动作的密度，也不能用一个尚未经过压缩变换的高斯密度代替。

| 数据或配置 | 通俗解释 | 在本例中 |
| --- | --- | --- |
| Actor 分布参数 | 决定动作往哪里集中、分散多少 | 每个观测产生连续动作分布 |
| 采样动作 | 从分布抽出的实际数值 | Pendulum 的一维扭矩 |
| 两个 Q | 对给定观测、动作的两份评分 | 各一个数，目标取小 |
| `ent_coef="auto"` | 学习熵项的权重 | 温度不是始终 0.2 |

SAC 的随机性来自策略本身；完整代码没有像 DDPG 那样必须另配 NormalActionNoise。评估使用 deterministic=True 是另一种选择动作方式，用于观察确定性评估表现，不能代表随机执行时所有可能的表现。

## 随机动作、密度与自动温度怎么接起来

Actor 先给一个高斯分布的均值和标准差，再采样、经 tanh 压缩成 [−1, 1] 内的归一化动作。内部 Critic 和熵使用这个动作坐标；送入 Pendulum 前才乘 2，变成环境扭矩。分布参数、抽到的动作和该动作点的密度是三种不同数据。

例如平均 log 密度为 1.5，平均负 log 密度即熵估计为 −1.5。完整脚本的目标熵为 −1，auto 会倾向增大熵权重，让策略优化更重视熵；若平均熵为 −0.5，则倾向降低权重。密度可能大于 1，不能把这里的 1.5 当作“概率超过 100%”。

tanh 压缩后必须修正密度；假设动作 x=0.6，压缩前 log 密度为 −1，修正后约为 −0.554。短片段给定的 −0.7 假设已经完成这种修正。具体公式与温度方向的单步计算见[本算法公式篇](../math/sac.md)。

## 看懂输出

- `Actual training steps`：实际交互步数；本例单环境、逐步采样，不需要凑齐 A2C/PPO 的固定长度片段。
- `Before`：未训练模型的确定性评估均值。
- `After`：保存并重新加载模型后，5 幕独立评估的均值与标准差。
- `rl-output/sac/model.zip`：模型文件；同目录的 `train.monitor.csv` 保存训练回合记录。

运行成功只说明接口与训练链路正常。判断学习效果还需要更充分的训练、更多评估回合和多个训练种子。

## 阅读练习：把理解分成三小步

<div class="practice-card" markdown="1">

<p class="practice-kicker">纸笔演算，不需要运行训练</p>

<p class="practice-title">每项熵信号都要对应同一个采样动作</p>

**沿用这些条件**：下一动作的两个目标 Q=1.8、1.5，对数密度 −0.7；温度 0.2、奖励 −1、折扣 0.9，未终止。

**从哪里开始**：回到本页的核心短片段，先圈出输入和旧预测，再计算临时目标；最后才判断要修改什么。

**按这几步做**：

1. 先取较小 Q，再计算减温度乘 log 密度。
2. 完成折扣与即时奖励两步。
3. 若真正终止，目标还含未来熵吗？auto 温度是否一直为 0.2？

??? tip "先要一点提示？"

    给每个数写上名字，区分奖励、旧预测、目标、参数或动作。每算完一步，把中间结果写下来，再进入下一步，不只抄最后答案。

??? example "对照完整推理"

    较小 Q=1.5；熵相关项为 −0.2×(−0.7)=0.14，软价值为 1.64；折扣后为 1.476，再加 −1，目标为 0.476。顺序是先把后续软价值算完整，再乘折扣。

    真正终止时没有未来 Q 或未来熵项，目标只剩奖励 −1。auto 会按实现学习温度，0.2 只是本例数字。对数密度必须对应这次采样并经过正确动作变换的同一个动作，不能随手换成别的概率。

</div>

## 第二遍再读完整脚本

先用上面的短片段和练习弄清更新目标，再展开脚本追踪“创建模型 → 训练 → 保存 → 重新加载 → 独立评估”。保存文件与命令行参数不参与算法公式。

??? note "展开带注释的完整脚本"

    ```python title="sac · 完整学习代码"
    """SAC 训练、保存与独立评估；默认 10000 步，可传 --steps 调整。"""
    # 命令行参数工具；阅读算法时可先跳过参数解析部分。
    import argparse
    from pathlib import Path
    # 环境接口库：提供 reset 开始一局、step 执行动作。
    import gymnasium as gym
    # 神经网络库；本示例的网络与梯度计算由 SB3 调用它完成。
    import torch
    # 导入库实现的算法；调用库并不等于从零实现算法内部。
    from stable_baselines3 import SAC
    from stable_baselines3.common.monitor import Monitor
    from stable_baselines3.common.evaluation import evaluate_policy


    def main(steps, seed):
        # 限制 CPU 计算线程数量，不代表启动机器人或仿真控制线程。
        torch.set_num_threads(1)
        # Path 表示文件路径；后面的 / 是拼接子路径，并非这里在做数字除法。
        output = Path("rl-output/sac")
        # 只有主动运行脚本才创建输出目录；网站展示代码不会执行这一行。
        output.mkdir(parents=True, exist_ok=True)
        # 训练环境负责收集经验，Monitor 统计每幕奖励与步数。
        train_env = Monitor(gym.make("Pendulum-v1"), str(output / "train"))
        # 另建评估环境，避免把训练过程中的奖励直接当作评估结果。
        eval_env = Monitor(gym.make("Pendulum-v1"))
        # 评估随机种子单独设置；它不保证跨硬件逐位一致。
        # reset 返回初始观测和 info；评估器之后会自行按回合调用环境接口。
        eval_env.reset(seed=seed + 100)
        try:
            # 创建策略与价值网络；初始化完成不意味着模型已经学会任务。
            model = SAC(
                # 多层感知机策略；seed 控制随机初始化，device 指定 CPU。
                "MlpPolicy", train_env, seed=seed, device="cpu", verbose=0,
                # 完整示例折扣固定为 0.99；正文短算例另给折扣，便于口算。
                gamma=0.99,
                # 经验回放容量、开始学习前的采样步数、每批样本数。
                buffer_size=20000, learning_starts=100, batch_size=64,
                # 每交互一步后进行一次梯度更新；训练初期先积累经验。
                train_freq=1, gradient_steps=1, ent_coef="auto",
                # auto 目标熵取负动作维数；本例是一维动作，所以目标为 -1。
                target_entropy="auto", tau=0.005,
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
            loaded = SAC.load(str(output / "model"), device="cpu")
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

[Stable-Baselines3：SAC](https://stable-baselines3.readthedocs.io/en/v2.9.0/modules/sac.html)
