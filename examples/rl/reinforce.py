"""标准库教学代码：对照注释理解更新过程，无需运行。"""
import math
import random

# 固定随机数起点，便于对照不同步骤；随机种子不保证跨硬件完全一致。
rng = random.Random(7)
# gamma 给未来奖励打折；本算法的更新步长在更新语句中定义。
gamma = 0.95

# 小走廊模型：输入当前位置与动作，返回下一位置、奖励、终止标记。
def step(state, action):
    # 动作 1 向右一步，动作 0 向左一步。
    ns = state + (1 if action == 1 else -1)
    # 走到两端才是真正终止；终止状态没有后续奖励。
    done = ns in (0, 6)
    # 右端奖励 +1、左端 -1，其余每步 -0.01，鼓励尽快到达右端。
    reward = 1.0 if ns == 6 else -1.0 if ns == 0 else -0.01
    return ns, reward, done


# 将动作偏好转换成概率；先减最大值可减少指数溢出的风险。
def softmax(row):
    weights = [math.exp(x - max(row)) for x in row]
    total = sum(weights)
    return [x / total for x in weights]

# 保存每个动作的偏好值，不是概率；softmax 后才得到概率。
logits = [[0.0, 0.0] for _ in range(7)]
# 外层控制迭代或采样幕数；数值只是教学配置，不是收敛保证。
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
        # 本步更新完以后，再移动当前位置；提前赋值会把旧状态的信息丢掉。
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
