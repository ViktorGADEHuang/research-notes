"""标准库教学代码：对照注释理解更新过程，无需运行。"""
import math
import random

# 固定随机数起点，便于对照不同步骤；随机种子不保证跨硬件完全一致。
rng = random.Random(7)
# gamma 给未来奖励打折；本算法的更新步长在更新语句中定义。
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


# 将动作偏好转换成概率；先减最大值可减少指数溢出的风险。
def softmax(row):
    largest = max(row)  # 同一行都减去同一个最大值，概率比例不变。
    weights = [math.exp(x - largest) for x in row]
    total = sum(weights)
    return [x / total for x in weights]

# 保存每个动作的偏好值，不是概率；softmax 后才得到概率。
logits = [[0.0, 0.0] for _ in range(7)]
# 采集 3000 个回合；每局结束后才整体更新一次策略偏好。
# 这些数量是教学设置，不构成收敛保证。
for _ in range(3000):
    # 一幕从状态 3 开始，并记录这一幕经历的数据。
    s, episode = 3, []
    # 持续与环境交互，直到走到左端或右端。
    while s not in (0, 6):
        # logits[s] 是当前状态的偏好；softmax 才把它转换为左右选择概率。
        probs = softmax(logits[s])
        # choices 返回列表；[0] 取出这一次抽到的动作编号，并非取最高概率。
        a = rng.choices([0, 1], weights=probs)[0]
        # 执行一次动作，获得下一状态、奖励和真正终止的标记。
        ns, reward, done = step(s, a)
        # 保存这一时刻的数据，方便在结束后从后往前计算回报。
        episode.append((s, a, reward))
        # 先保存动作前的位置，再推进当前位置；本局学习要等回合结束。
        s = ns
    # 只创建本局的回报表；最后一步之后回报为 0，便于从末尾递推。
    returns, total = [0.0] * len(episode), 0.0
    # 从最后一步倒推 G：当前奖励 + gamma × 后面已经算好的回报。
    for t in reversed(range(len(episode))):
        total = episode[t][2] + gamma * total
        returns[t] = total
    # 为这一幕创建梯度累积表；先不改变策略偏好。
    grad = [[0.0, 0.0] for _ in range(7)]
    for t, (s, a, _) in enumerate(episode):
        # logits[s] 是当前状态的偏好；softmax 才把它转换为左右选择概率。
        probs = softmax(logits[s])
        for j in range(2):
            # softmax 的 log 概率梯度是“是否选了 j - j 的概率”，再乘折扣权重与回报。
            grad[s][j] += gamma**t * returns[t] * ((j == a) - probs[j])
    # 算完一整幕的旧策略梯度后再更新参数。
    for s in range(1, 6):
        for a in range(2):
            # 梯度上升提高期望回报；这里学习率 0.02 是教学参数。
            logits[s][a] += 0.02 * grad[s][a]
print("P(right):", [round(softmax(logits[s])[1], 3) for s in range(1, 6)])
