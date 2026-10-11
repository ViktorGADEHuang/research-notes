
# PPO 强化学习算法

## 1. PPO 是什么？

PPO 是一种强化学习算法。

简单来说，就是让机器人通过不断尝试，
逐渐学会做出更好的决策。

## 2. PPO 在放牧机器人中的应用

假设我们有一台宇树 Go2 机器人。

机器人可以观察：

- 羊群的位置
- 羊群的运动方向
- 目标区域的位置

机器人可以输出：

- 前进速度
- 横向速度
- 转向角速度

通过奖励机制，让机器人学习如何驱赶羊群。

## 3. Python 代码

```python
from stable_baselines3 import PPO

model = PPO(
    "MlpPolicy",
    env,
    verbose=1
)

model.learn(total_timesteps=100000)
```

## 4. 学习心得

这里记录自己对 PPO 算法的理解。
