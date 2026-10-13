"""DDPG 训练、保存与独立评估；默认 10000 步，可传 --steps 调整。"""
# 命令行参数工具；阅读算法时可先跳过参数解析部分。
import argparse
from pathlib import Path
# 环境接口库：提供 reset 开始一局、step 执行动作。
import gymnasium as gym
# 数组计算工具；这里主要用于连续动作的探索噪声。
import numpy as np
# 神经网络库；本示例的网络与梯度计算由 SB3 调用它完成。
import torch
# 导入库实现的算法；调用库并不等于从零实现算法内部。
from stable_baselines3 import DDPG
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.noise import NormalActionNoise


def main(steps, seed):
    # 限制 CPU 计算线程数量，不代表启动机器人或仿真控制线程。
    torch.set_num_threads(1)
    # Path 表示文件路径；后面的 / 是拼接子路径，并非这里在做数字除法。
    output = Path("rl-output/ddpg")
    # 只有主动运行脚本才创建输出目录；网站展示代码不会执行这一行。
    output.mkdir(parents=True, exist_ok=True)
    # 训练环境负责收集经验，Monitor 统计每幕奖励与步数。
    train_env = Monitor(gym.make("Pendulum-v1"), str(output / "train"))
    # 另建评估环境，避免把训练过程中的奖励直接当作评估结果。
    eval_env = Monitor(gym.make("Pendulum-v1"))
    # 评估随机种子单独设置；它不保证跨硬件逐位一致。
    # reset 返回初始观测和 info；评估器之后会自行按回合调用环境接口。
    eval_env.reset(seed=seed + 100)
    dim = train_env.action_space.shape[0]
    # 探索噪声加在 [-1, 1] 归一化动作上；换回 Pendulum 扭矩需再乘 2。
    noise = NormalActionNoise(mean=np.zeros(dim), sigma=0.1 * np.ones(dim))
    try:
        # 创建策略与价值网络；初始化完成不意味着模型已经学会任务。
        model = DDPG(
            # 多层感知机策略；seed 控制随机初始化，device 指定 CPU。
            "MlpPolicy", train_env, seed=seed, device="cpu", verbose=0,
            # 完整示例折扣固定为 0.99；正文短算例另给折扣，便于口算。
            gamma=0.99,
            # 经验回放容量、开始学习前的采样步数、每批样本数。
            buffer_size=20000, learning_starts=100, batch_size=64,
            # 每交互一步后进行一次梯度更新；训练初期先积累经验。
            train_freq=1, gradient_steps=1, action_noise=noise,
            # 每次把当前参数的 0.5% 混入目标参数；不是把动作减小 0.5%。
            tau=0.005,
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
        loaded = DDPG.load(str(output / "model"), device="cpu")
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
