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

q = [[0.0, 0.0] for _ in range(7)]
for _ in range(3000):
    s = 3
    a = choose(q, s)
    while s not in (0, 6):
        ns, reward, done = step(s, a)
        next_action = choose(q, ns) if not done else 0
        target = reward + (0.0 if done else gamma * q[ns][next_action])
        q[s][a] += alpha * (target - q[s][a])
        s, a = ns, next_action  # 下一步执行的就是这个 next_action
print("Q:", [[round(x, 3) for x in row] for row in q[1:6]])
print("Greedy actions:", [max(range(2), key=lambda a: q[s][a]) for s in range(1, 6)])
