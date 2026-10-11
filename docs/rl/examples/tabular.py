"""Python 标准库实现：价值迭代、MC、TD(0)、SARSA、Q-learning、REINFORCE。

运行：python tabular.py q-learning
小环境为长度为 6 的走廊；右端终止奖励 +1，左端终止奖励 -1。
"""
import argparse
import math
import random


def step(state, action):
    next_state = state + (1 if action == 1 else -1)
    done = next_state in (0, 6)
    reward = 1.0 if next_state == 6 else -1.0 if next_state == 0 else -0.01
    return next_state, reward, done


def choose(q, state, rng, epsilon=0.15):
    if rng.random() < epsilon:
        return rng.randrange(2)
    best = max(q[state])
    return rng.choice([a for a in range(2) if q[state][a] == best])


def softmax(row):
    weights = [math.exp(x - max(row)) for x in row]
    return [x / sum(weights) for x in weights]


def run(algorithm, episodes=3000, seed=7):
    rng = random.Random(seed)
    gamma, alpha = 0.95, 0.1
    values = [0.0] * 7
    q = [[0.0, 0.0] for _ in range(7)]
    counts = [0] * 7
    logits = [[0.0, 0.0] for _ in range(7)]

    if algorithm == "value-iteration":
        for _ in range(10000):
            old = values[:]
            for state in range(1, 6):
                targets = []
                for action in range(2):
                    ns, reward, done = step(state, action)
                    targets.append(reward + (0.0 if done else gamma * old[ns]))
                values[state] = max(targets)
            if max(abs(x - y) for x, y in zip(values, old)) < 1e-10:
                break
        print("Optimal values:", [round(x, 3) for x in values])
        return {"values": values}

    for _ in range(episodes):
        state = 3
        trajectory = []
        action = choose(q, state, rng)
        # 本例走到终点才结束，不把人为超时当成真实终止。
        while state not in (0, 6):
            if algorithm in ("mc", "td"):
                action = rng.randrange(2)  # 评估同一个均匀随机策略
            elif algorithm == "reinforce":
                probs = softmax(logits[state])
                action = rng.choices([0, 1], weights=probs)[0]
            elif algorithm == "q-learning":
                action = choose(q, state, rng)
            ns, reward, done = step(state, action)
            trajectory.append((state, action, reward))
            if algorithm == "td":
                target = reward + (0.0 if done else gamma * values[ns])
                values[state] += alpha * (target - values[state])
            elif algorithm in ("sarsa", "q-learning"):
                next_action = choose(q, ns, rng) if not done else 0
                future = q[ns][next_action] if algorithm == "sarsa" else max(q[ns])
                target = reward + (0.0 if done else gamma * future)
                q[state][action] += alpha * (target - q[state][action])
                action = next_action
            state = ns

        if algorithm in ("mc", "reinforce"):
            returns = [0.0] * len(trajectory)
            total = 0.0
            for t in reversed(range(len(trajectory))):
                total = trajectory[t][2] + gamma * total
                returns[t] = total
            visited = set()
            # REINFORCE 梯度都在采样时的策略上计算，然后整体更新。
            gradients = [[0.0, 0.0] for _ in range(7)]
            for t, (s, a, _) in enumerate(trajectory):
                if algorithm == "mc" and s not in visited:
                    visited.add(s)  # 首次访问 MC：每幕只统计第一次出现
                    counts[s] += 1
                    values[s] += (returns[t] - values[s]) / counts[s]
                elif algorithm == "reinforce":
                    probs = softmax(logits[s])
                    for j in range(2):
                        gradients[s][j] += gamma**t * returns[t] * ((j == a) - probs[j])
            if algorithm == "reinforce":
                for s in range(1, 6):
                    for a in range(2):
                        logits[s][a] += 0.02 * gradients[s][a]

    if algorithm in ("mc", "td"):
        print("Random-policy values:", [round(x, 3) for x in values])
    elif algorithm == "reinforce":
        print("P(right):", [round(softmax(logits[s])[1], 3) for s in range(1, 6)])
    else:
        print("Q table:", [[round(x, 3) for x in row] for row in q[1:6]])
        print("Greedy actions (0=left, 1=right):", [max(range(2), key=lambda a: q[s][a]) for s in range(1, 6)])
    return {"values": values, "q": q, "logits": logits}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("algorithm", choices=["value-iteration", "mc", "td", "sarsa", "q-learning", "reinforce"])
    parser.add_argument("--episodes", type=int, default=3000)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()
    run(args.algorithm, args.episodes, args.seed)
