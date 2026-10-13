"""运行真实 SB3 训练：python deep_rl.py ppo --steps 10000。"""
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
from stable_baselines3 import A2C, DDPG, DQN, PPO, SAC, TD3
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.noise import NormalActionNoise


def run(algorithm, steps=10000, seed=7, output="rl-output"):
    # 限制 CPU 计算线程数量，不代表启动机器人或仿真控制线程。
    torch.set_num_threads(1)
    classes = {"dqn": DQN, "a2c": A2C, "ppo": PPO, "ddpg": DDPG, "td3": TD3, "sac": SAC}
    env_id = "Pendulum-v1" if algorithm in ("ddpg", "td3", "sac") else "CartPole-v1"
    output_dir = Path(output) / algorithm
    # 只有运行脚本才会生成日志与模型文件；阅读本页无需创建目录。
    output_dir.mkdir(parents=True, exist_ok=True)
    # 训练环境负责收集经验，Monitor 统计每幕奖励与步数。
    train_env = Monitor(gym.make(env_id), str(output_dir / "train"))
    # 另建评估环境，避免把训练过程中的奖励直接当作评估结果。
    eval_env = Monitor(gym.make(env_id))
    # 评估随机种子单独设置；它不保证跨硬件逐位一致。
    # reset 返回初始观测和 info；评估器之后会自行按回合调用环境接口。
    eval_env.reset(seed=seed + 100)
    kwargs = {"seed": seed, "device": "cpu", "verbose": 0, "gamma": 0.99}
    if algorithm in ("dqn", "ddpg", "td3", "sac"):
        # 经验回放容量、开始学习前的采样步数、每批样本数。
        kwargs.update(buffer_size=20000, learning_starts=100, batch_size=64,
                      # 决定多频繁学习与每次做多少梯度更新；SAC auto 自动调节熵系数。
                      train_freq=1, gradient_steps=1)
    if algorithm == "dqn":
        kwargs.update(target_update_interval=250, exploration_fraction=0.3,
                      exploration_initial_eps=1.0, exploration_final_eps=0.05)
    elif algorithm == "a2c":
        # 采集长度决定一次更新前收集多少步；PPO 还会分小批量重复更新。
        kwargs.update(n_steps=32, gae_lambda=1.0, normalize_advantage=False, ent_coef=0.0)
    elif algorithm == "ppo":
        # 采集长度决定一次更新前收集多少步；PPO 还会分小批量重复更新。
        kwargs.update(n_steps=256, batch_size=64, n_epochs=4, clip_range=0.2,
                      gae_lambda=0.95, normalize_advantage=True, ent_coef=0.0)
    elif algorithm in ("ddpg", "td3"):
        # shape[0] 查动作数组长度；Pendulum 的动作是一维，观测却有三维。
        action_dim = train_env.action_space.shape[0]
        # 软更新与归一化动作噪声；它们不是机器人接口的物理单位。
        kwargs["tau"] = 0.005
        if algorithm == "td3":
            kwargs.update(policy_delay=2, target_policy_noise=0.2, target_noise_clip=0.5)
        kwargs["action_noise"] = NormalActionNoise(
            # 每个动作维度使用零均值高斯噪声，标准差设为 0.1。
            mean=np.zeros(action_dim), sigma=0.1 * np.ones(action_dim))
    elif algorithm == "sac":
        kwargs.update(ent_coef="auto", target_entropy="auto", tau=0.005)

    try:
        # 按所选算法建立模型：DQN 使用 Q 网络，其他列出的算法使用 Actor/Critic。
        model = classes[algorithm]("MlpPolicy", train_env, **kwargs)
        # 记录未训练策略的评估均值，作为观察起点。
        # 左边两个名字接收均值和标准差；这里用 _ 表示暂时不使用第二项。
        before, _ = evaluate_policy(model, eval_env, n_eval_episodes=5, deterministic=True)
        # 这行才触发训练；本教程只提供代码，不在项目中自动调用。
        model.learn(total_timesteps=steps)
        model_path = output_dir / "model"
        # 保存参数，便于理解模型持久化，不表示策略性能已达标。
        model.save(str(model_path))
        # 验证保存后的模型能重新加载，并在独立环境中评估。
        # 从磁盘重新加载模型，展示部署前参数恢复的步骤。
        loaded = classes[algorithm].load(str(model_path), device="cpu")
        # 评估随机种子单独设置；它不保证跨硬件逐位一致。
        eval_env.reset(seed=seed + 100)
        # 使用独立环境评估恢复的模型，输出平均回报与标准差。
        # std 是这些评估回合回报的标准差，不是训练结果可靠性的保证。
        after, std = evaluate_policy(loaded, eval_env, n_eval_episodes=5, deterministic=True)
        print(f"{algorithm.upper()} | {env_id} | steps={model.num_timesteps}")
        print(f"before={before:.2f} | after={after:.2f} +/- {std:.2f}")
        print(f"Saved: {model_path}.zip")
        return {"before": before, "after": after, "steps": model.num_timesteps}
    # 即使中间发生异常，也尝试释放环境资源。
    finally:
        train_env.close()
        eval_env.close()


# 入口保护：被导入时不调用这里的 main；网站只展示文本。
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("algorithm", choices=["dqn", "a2c", "ppo", "ddpg", "td3", "sac"])
    # steps 是训练预算示例，不是预期学会任务所需的精确步数。
    parser.add_argument("--steps", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--output", default="rl-output")
    # 把可选命令行文字转换为参数值；定义参数本身不会启动学习。
    args = parser.parse_args()
    if args.steps <= 0:
        parser.error("--steps must be positive")
    run(args.algorithm, args.steps, args.seed, args.output)
