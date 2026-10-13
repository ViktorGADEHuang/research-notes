"""标准库教学代码：对照注释理解更新过程，无需运行。"""
import random

# 固定随机数起点，便于对照不同步骤；随机种子不保证跨硬件完全一致。
rng = random.Random(7)
# gamma 给未来奖励打折；alpha 决定每次向目标修正多少。
gamma, alpha = 0.95, 0.1

# 小走廊模型：输入当前位置与动作，返回下一位置、奖励、终止标记。
def step(state, action):
    # 调用者只传动作 0 或 1；先按动作找到下一位置。
    if action == 1:
        ns = state + 1  # 向右。
    else:
        ns = state - 1  # 向左。
    # 两端才是真正终点；0、6 不再作为下一次 step 的输入。
    done = ns in (0, 6)
    # 奖励描述刚发生的结果；进入终点时不再额外扣中间步进代价。
    if ns == 6:
        reward = 1.0
    elif ns == 0:
        reward = -1.0
    else:
        reward = -0.01
    return ns, reward, done


# V 表按状态存分数；两个终止位置也占位，但不更新它们。
# 下标就是状态编号；0 与 6 作为终点占位，非终止位置是 1 到 5。
values = [0.0] * 7
# 采集 10000 个回合；每走一步就修正一次 V，策略始终随机。
# 这些数量是教学设置，不构成收敛保证。
for _ in range(10000):
    # 每一局从位置 3 重新出发；外面的 V/Q 表不重置，所以能积累经验。
    s = 3
    # 持续与环境交互，直到走到左端或右端。
    while s not in (0, 6):
        a = rng.randrange(2)  # 与 MC 使用同一随机策略
        # 执行一次动作，获得下一状态、奖励和真正终止的标记。
        ns, reward, done = step(s, a)
        # 目标 = 本步奖励 + 折扣后的后续估计；done 时后续项归零。
        target = reward + (0.0 if done else gamma * values[ns])
        # TD 每走一步就更新 V，无需等到这一幕结束。
        values[s] += alpha * (target - values[s])
        # 本步更新完以后，再移动当前位置；提前赋值会把旧状态的信息丢掉。
        s = ns
print("Random-policy values:", [round(x, 3) for x in values[1:6]])
