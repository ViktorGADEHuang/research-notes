"""标准库教学代码：对照注释理解更新过程，无需运行。"""

# gamma 给未来奖励打折；价值迭代每轮直接采用最大的动作目标。
gamma = 0.95

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
values = [0.0] * 7
# 最多做 10000 轮计算；每轮重算五个位置，不与环境采样交互。
# 这些数量是教学设置，不构成收敛保证。
for _ in range(10000):
    # 复制上一轮的 V；本轮所有目标都使用旧表，进行同步更新。
    # 本表元素是不可变数字，切片得到独立列表，写 values 不会改 old。
    old = values[:]
    for s in range(1, 6):
        candidates = []
        for a in range(2):
            # 用已知规则计算候选动作的结果；这里是在枚举，不是采样。
            ns, reward, done = step(s, a)
            # 比较两种动作的“一步奖励 + 下一状态价值”，不是随机采样。
            candidates.append(reward + (0.0 if done else gamma * old[ns]))
        # 价值迭代选择当前最大的候选目标，逼近最优状态价值。
        values[s] = max(candidates)
    # 比较新旧表的最大变化；足够小则停止迭代。
    if max(abs(x - y) for x, y in zip(values, old)) < 1e-10:
        break
policy = []
for s in range(1, 6):
    candidates = []
    for a in range(2):
        # 用已知规则计算候选动作的结果；这里是在枚举，不是采样。
        ns, reward, done = step(s, a)
        # 比较两种动作的“一步奖励 + 下一状态价值”，不是随机采样。
        candidates.append(reward + (0.0 if done else gamma * values[ns]))
    policy.append(max(range(2), key=lambda a: candidates[a]))
print("Values:", [round(x, 3) for x in values[1:6]])
print("Actions (0=left, 1=right):", policy)
