"""Python 标准库实现：价值迭代、MC、TD(0)、SARSA、Q-learning、REINFORCE。

阅读时先看 step 定义，再找到所选算法的目标值与更新语句。
小环境为长度为 6 的走廊；右端终止奖励 +1，左端终止奖励 -1。
"""
# 命令行参数工具；阅读算法时可先跳过参数解析部分。
import argparse
import math
import random


# 小走廊模型：输入当前位置与动作，返回下一位置、奖励、终止标记。
def step(state, action):
    # 动作 1 向右一步，动作 0 向左一步。
    next_state = state + (1 if action == 1 else -1)
    # 走到两端才是真正终止；终止状态没有后续奖励。
    done = next_state in (0, 6)
    # 右端奖励 +1、左端 -1，其余每步 -0.01，鼓励尽快到达右端。
    reward = 1.0 if next_state == 6 else -1.0 if next_state == 0 else -0.01
    return next_state, reward, done


# epsilon-greedy：少量随机探索，多数时候选择当前高分动作。
def choose(q, state, rng, epsilon=0.15):
    # 以 epsilon 的概率探索，防止一直停在当前看起来最好的选择。
    if rng.random() < epsilon:
        return rng.randrange(2)
    # 取当前状态的最高 Q 值；相同分数的动作随机打破平局。
    best = max(q[state])
    return rng.choice([a for a in range(2) if q[state][a] == best])


# 将动作偏好转换成概率；先减最大值可减少指数溢出的风险。
def softmax(row):
    weights = [math.exp(x - max(row)) for x in row]
    return [x / sum(weights) for x in weights]


def run(algorithm, episodes=3000, seed=7):
    # 固定随机数起点，便于对照不同步骤；随机种子不保证跨硬件完全一致。
    rng = random.Random(seed)
    # gamma 给未来奖励打折；alpha 决定每次向目标修正多少。
    gamma, alpha = 0.95, 0.1
    # V 表按状态存分数；两个终止位置也占位，但不更新它们。
    values = [0.0] * 7
    # Q 表每行对应状态，两列分别对应向左与向右。
    # 每行分别创建新列表；不能写 [[0.0, 0.0]] * 7，那会让七行共用同一列表。
    q = [[0.0, 0.0] for _ in range(7)]
    # 记录每个状态被纳入平均的次数，用于首次访问 MC。
    counts = [0] * 7
    # 保存每个动作的偏好值，不是概率；softmax 后才得到概率。
    logits = [[0.0, 0.0] for _ in range(7)]

    if algorithm == "value-iteration":
        # 外层控制迭代或采样幕数；数值只是教学配置，不是收敛保证。
        for _ in range(10000):
            # 复制上一轮的 V；本轮所有目标都使用旧表，进行同步更新。
            old = values[:]
            for state in range(1, 6):
                targets = []
                for action in range(2):
                    # 执行一次动作，获得下一状态、奖励和真正终止的标记。
                    ns, reward, done = step(state, action)
                    targets.append(reward + (0.0 if done else gamma * old[ns]))
                values[state] = max(targets)
            # 比较新旧表的最大变化；足够小则停止迭代。
            if max(abs(x - y) for x, y in zip(values, old)) < 1e-10:
                break
        print("Optimal values:", [round(x, 3) for x in values])
        return {"values": values}

    # 外层控制迭代或采样幕数；数值只是教学配置，不是收敛保证。
    for _ in range(episodes):
        state = 3
        trajectory = []
        action = choose(q, state, rng)
        # 本例走到终点才结束，不把人为超时当成真实终止。
        while state not in (0, 6):
            if algorithm in ("mc", "td"):
                action = rng.randrange(2)  # 评估同一个均匀随机策略
            elif algorithm == "reinforce":
                # 查询本状态的动作分布，再从中随机抽取一个动作。
                probs = softmax(logits[state])
                action = rng.choices([0, 1], weights=probs)[0]
            elif algorithm == "q-learning":
                action = choose(q, state, rng)
            # 执行一次动作，获得下一状态、奖励和真正终止的标记。
            ns, reward, done = step(state, action)
            # 记下状态、动作与奖励，MC/REINFORCE 要在一幕结束后回看。
            trajectory.append((state, action, reward))
            if algorithm == "td":
                # 目标 = 本步奖励 + 折扣后的后续估计；done 时后续项归零。
                target = reward + (0.0 if done else gamma * values[ns])
                # 一步 TD：用下一状态当前估计构造目标，然后修正当前估计。
                values[state] += alpha * (target - values[state])
            elif algorithm in ("sarsa", "q-learning"):
                # SARSA 用下一步实际准备执行的动作；终止时的占位动作不参与目标。
                next_action = choose(q, ns, rng) if not done else 0
                future = q[ns][next_action] if algorithm == "sarsa" else max(q[ns])
                # 目标 = 本步奖励 + 折扣后的后续估计；done 时后续项归零。
                target = reward + (0.0 if done else gamma * future)
                # 只更新本次访问的 Q 格；目标定义区分 SARSA 与 Q-learning。
                q[state][action] += alpha * (target - q[state][action])
                action = next_action
            state = ns

        if algorithm in ("mc", "reinforce"):
            returns = [0.0] * len(trajectory)
            total = 0.0
            # 从最后一步倒推 G：当前奖励 + gamma × 后面已经算好的回报。
            for t in reversed(range(len(trajectory))):
                total = trajectory[t][2] + gamma * total
                returns[t] = total
            # 同一幕内用集合标记出现过的状态，保证首次访问 MC 不重复计数。
            visited = set()
            # REINFORCE 梯度都在采样时的策略上计算，然后整体更新。
            # 为这一幕创建梯度累积表；先不改变策略偏好。
            gradients = [[0.0, 0.0] for _ in range(7)]
            for t, (s, a, _) in enumerate(trajectory):
                if algorithm == "mc" and s not in visited:
                    visited.add(s)  # 首次访问 MC：每幕只统计第一次出现
                    counts[s] += 1
                    # 用增量平均吸收这一幕的回报；步长是 1 / 访问次数。
                    values[s] += (returns[t] - values[s]) / counts[s]
                elif algorithm == "reinforce":
                    probs = softmax(logits[s])
                    for j in range(2):
                        # 折扣权重 × 回报 × log 策略梯度；这是无基线 REINFORCE。
                        gradients[s][j] += gamma**t * returns[t] * ((j == a) - probs[j])
            if algorithm == "reinforce":
                for s in range(1, 6):
                    for a in range(2):
                        # 梯度上升提高期望回报；这里学习率 0.02 是教学参数。
                        logits[s][a] += 0.02 * gradients[s][a]

    if algorithm in ("mc", "td"):
        print("Random-policy values:", [round(x, 3) for x in values])
    elif algorithm == "reinforce":
        print("P(right):", [round(softmax(logits[s])[1], 3) for s in range(1, 6)])
    else:
        print("Q table:", [[round(x, 3) for x in row] for row in q[1:6]])
        print("Greedy actions (0=left, 1=right):", [max(range(2), key=lambda a: q[s][a]) for s in range(1, 6)])
    return {"values": values, "q": q, "logits": logits}


# 入口保护：被导入时不调用这里的 main；网站只展示文本。
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("algorithm", choices=["value-iteration", "mc", "td", "sarsa", "q-learning", "reinforce"])
    parser.add_argument("--episodes", type=int, default=3000)
    parser.add_argument("--seed", type=int, default=7)
    # 把可选命令行文字转换为参数值；定义参数本身不会启动学习。
    args = parser.parse_args()
    run(args.algorithm, args.episodes, args.seed)
