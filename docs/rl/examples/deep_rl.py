"""运行真实 SB3 训练：python deep_rl.py ppo --steps 10000。"""
import argparse
from pathlib import Path

import gymnasium as gym
import numpy as np
import torch
from stable_baselines3 import A2C, DDPG, DQN, PPO, SAC, TD3
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.noise import NormalActionNoise


def run(algorithm, steps=10000, seed=7, output="rl-output"):
    torch.set_num_threads(1)
    classes = {"dqn": DQN, "a2c": A2C, "ppo": PPO, "ddpg": DDPG, "td3": TD3, "sac": SAC}
    env_id = "Pendulum-v1" if algorithm in ("ddpg", "td3", "sac") else "CartPole-v1"
    output_dir = Path(output) / algorithm
    output_dir.mkdir(parents=True, exist_ok=True)
    train_env = Monitor(gym.make(env_id), str(output_dir / "train"))
    eval_env = Monitor(gym.make(env_id))
    eval_env.reset(seed=seed + 100)
    kwargs = {"seed": seed, "device": "cpu", "verbose": 0}
    if algorithm in ("dqn", "ddpg", "td3", "sac"):
        kwargs.update(buffer_size=20000, learning_starts=100, batch_size=64,
                      train_freq=1, gradient_steps=1)
    if algorithm == "dqn":
        kwargs.update(target_update_interval=250, exploration_fraction=0.3)
    elif algorithm == "a2c":
        kwargs.update(n_steps=32)
    elif algorithm == "ppo":
        kwargs.update(n_steps=256, batch_size=64, n_epochs=4, clip_range=0.2)
    elif algorithm in ("ddpg", "td3"):
        action_dim = train_env.action_space.shape[0]
        kwargs["action_noise"] = NormalActionNoise(
            mean=np.zeros(action_dim), sigma=0.1 * np.ones(action_dim))
    elif algorithm == "sac":
        kwargs["ent_coef"] = "auto"

    try:
        model = classes[algorithm]("MlpPolicy", train_env, **kwargs)
        before, _ = evaluate_policy(model, eval_env, n_eval_episodes=5, deterministic=True)
        model.learn(total_timesteps=steps)
        model_path = output_dir / "model"
        model.save(str(model_path))
        # 验证保存后的模型能重新加载，并在独立环境中评估。
        loaded = classes[algorithm].load(str(model_path), device="cpu")
        eval_env.reset(seed=seed + 100)
        after, std = evaluate_policy(loaded, eval_env, n_eval_episodes=5, deterministic=True)
        print(f"{algorithm.upper()} | {env_id} | steps={model.num_timesteps}")
        print(f"before={before:.2f} | after={after:.2f} +/- {std:.2f}")
        print(f"Saved: {model_path}.zip")
        return {"before": before, "after": after, "steps": model.num_timesteps}
    finally:
        train_env.close()
        eval_env.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("algorithm", choices=["dqn", "a2c", "ppo", "ddpg", "td3", "sac"])
    parser.add_argument("--steps", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--output", default="rl-output")
    args = parser.parse_args()
    if args.steps <= 0:
        parser.error("--steps must be positive")
    run(args.algorithm, args.steps, args.seed, args.output)
