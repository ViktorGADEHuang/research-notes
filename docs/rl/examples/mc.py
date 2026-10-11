"""标准库教学示例；运行本文件即可，不需要安装第三方依赖。"""
import math
import random

rng = random.Random(7)
gamma, alpha = 0.95, 0.1

def step(state, action):
    ns = state + (1 if action == 1 else -1)
    done = ns in (0, 6)
    reward = 1.0 if ns == 6 else -1.0 if ns == 0 else -0.01
    return ns, reward, done

def choose(q, state, epsilon=0.15):
    if rng.random() < epsilon:
        return rng.randrange(2)
    best = max(q[state])
    return rng.choice([a for a in range(2) if q[state][a] == best])

values = [0.0] * 7
counts = [0] * 7
for _ in range(10000):
    s, episode = 3, []
    while s not in (0, 6):
        a = rng.randrange(2)  # 只评估随机策略，不改进策略
        ns, reward, done = step(s, a)
        episode.append((s, reward))
        s = ns
    returns, total = [0.0] * len(episode), 0.0
    for t in reversed(range(len(episode))):
        total = episode[t][1] + gamma * total
        returns[t] = total
    visited = set()
    for t, (s, _) in enumerate(episode):
        if s not in visited:
            visited.add(s)
            counts[s] += 1
            values[s] += (returns[t] - values[s]) / counts[s]
print("Random-policy values:", [round(x, 3) for x in values[1:6]])
