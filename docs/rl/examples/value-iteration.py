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
for _ in range(10000):
    old = values[:]
    for s in range(1, 6):
        candidates = []
        for a in range(2):
            ns, reward, done = step(s, a)
            candidates.append(reward + (0.0 if done else gamma * old[ns]))
        values[s] = max(candidates)
    if max(abs(x - y) for x, y in zip(values, old)) < 1e-10:
        break
policy = []
for s in range(1, 6):
    candidates = []
    for a in range(2):
        ns, reward, done = step(s, a)
        candidates.append(reward + (0.0 if done else gamma * values[ns]))
    policy.append(max(range(2), key=lambda a: candidates[a]))
print("Values:", [round(x, 3) for x in values[1:6]])
print("Actions (0=left, 1=right):", policy)
