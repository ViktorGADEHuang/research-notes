"""SAC 训练、保存与独立评估；默认 10000 步，可传 --steps 调整。"""
import argparse
from pathlib import Path
import gymnasium as gym
import numpy as np
import torch
from stable_baselines3 import SAC
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.evaluation import evaluate_policy


def main(steps, seed):
    torch.set_num_threads(1)
    output = Path("rl-output/sac")
    output.mkdir(parents=True, exist_ok=True)
    train_env = Monitor(gym.make("Pendulum-v1"), str(output / "train"))
    eval_env = Monitor(gym.make("Pendulum-v1"))
    eval_env.reset(seed=seed + 100)
    try:
        model = SAC(
            "MlpPolicy", train_env, seed=seed, device="cpu", verbose=0,
            buffer_size=20000, learning_starts=100, batch_size=64,
        train_freq=1, gradient_steps=1, ent_coef="auto",
        )
        before, _ = evaluate_policy(model, eval_env, n_eval_episodes=5,
                                   deterministic=True)
        model.learn(total_timesteps=steps)
        model.save(str(output / "model"))
        loaded = SAC.load(str(output / "model"), device="cpu")
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
