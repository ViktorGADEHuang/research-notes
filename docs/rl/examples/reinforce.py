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

def softmax(row):
    weights = [math.exp(x - max(row)) for x in row]
    total = sum(weights)
    return [x / total for x in weights]

logits = [[0.0, 0.0] for _ in range(7)]
for _ in range(3000):
    s, episode = 3, []
    while s not in (0, 6):
        probs = softmax(logits[s])
        a = rng.choices([0, 1], weights=probs)[0]
        ns, reward, done = step(s, a)
        episode.append((s, a, reward))
        s = ns
    returns, total = [0.0] * len(episode), 0.0
    for t in reversed(range(len(episode))):
        total = episode[t][2] + gamma * total
        returns[t] = total
    grad = [[0.0, 0.0] for _ in range(7)]
    for t, (s, a, _) in enumerate(episode):
        probs = softmax(logits[s])
        for j in range(2):
            grad[s][j] += gamma**t * returns[t] * ((j == a) - probs[j])
    # 算完一整幕的旧策略梯度后再更新参数。
    for s in range(1, 6):
        for a in range(2):
            logits[s][a] += 0.02 * grad[s][a]
print("P(right):", [round(softmax(logits[s])[1], 3) for s in range(1, 6)])
