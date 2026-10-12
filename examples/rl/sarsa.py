"""标准库教学代码：对照注释理解更新过程，无需运行。"""
import random

# 固定随机数起点，便于对照不同步骤；随机种子不保证跨硬件完全一致。
rng = random.Random(7)
# gamma 给未来奖励打折；alpha 决定每次向目标修正多少。
gamma, alpha = 0.95, 0.1

# 小走廊模型：输入当前位置与动作，返回下一位置、奖励、终止标记。
def step(state, action):
    # 动作 1 向右一步，动作 0 向左一步。
    ns = state + (1 if action == 1 else -1)
    # 走到两端才是真正终止；终止状态没有后续奖励。
    done = ns in (0, 6)
    # 右端奖励 +1、左端 -1，其余每步 -0.01，鼓励尽快到达右端。
    reward = 1.0 if ns == 6 else -1.0 if ns == 0 else -0.01
    return ns, reward, done

# epsilon-greedy：少量随机探索，多数时候选择当前高分动作。
def choose(q, state, epsilon=0.15):
    # 以 epsilon 的概率探索，防止一直停在当前看起来最好的选择。
    if rng.random() < epsilon:
        return rng.randrange(2)
    # 取当前状态的最高 Q 值；相同分数的动作随机打破平局。
    best = max(q[state])
    return rng.choice([a for a in range(2) if q[state][a] == best])

# Q 表每行对应状态，两列分别对应向左与向右。
q = [[0.0, 0.0] for _ in range(7)]
# 外层控制迭代或采样幕数；数值只是教学配置，不是收敛保证。
for _ in range(3000):
    # 每一局从位置 3 重新出发；外面的 V/Q 表不重置，所以能积累经验。
    s = 3
    a = choose(q, s)
    # 持续与环境交互，直到走到左端或右端。
    while s not in (0, 6):
        # 执行一次动作，获得下一状态、奖励和真正终止的标记。
        ns, reward, done = step(s, a)
        # SARSA 用下一步实际准备执行的动作；终止时的占位动作不参与目标。
        next_action = choose(q, ns) if not done else 0
        # 目标 = 本步奖励 + 折扣后的后续估计；done 时后续项归零。
        target = reward + (0.0 if done else gamma * q[ns][next_action])
        # Q 更新：旧值 + 学习率 ×（目标 - 旧值），只改刚执行的状态动作格。
        q[s][a] += alpha * (target - q[s][a])
        s, a = ns, next_action  # 下一步执行的就是这个 next_action
print("Q:", [[round(x, 3) for x in row] for row in q[1:6]])
print("Greedy actions:", [max(range(2), key=lambda a: q[s][a]) for s in range(1, 6)])
