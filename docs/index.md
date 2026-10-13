---
 title: 首页
 hide:
   - navigation
   - toc
---

<div class="research-hero" markdown="1">

<p class="hero-kicker">VIKTOR / RESEARCH NOTEBOOK</p>

# Viktor’s Research Notes

这里记录我的科研与技术学习笔记。目前的研究方向是 **放牧机器人**，同时整理强化学习、机器人技术、计算机视觉与编程方面的学习内容。

<div class="hero-actions" markdown="1">

[放牧机器人研究 →](herding/index.md){ .hero-btn .hero-btn-primary }
[浏览学习笔记](#learning-notes){ .hero-btn .hero-btn-outline }

</div>

<p class="hero-bottom">科研记录 · 学习笔记 · 论文阅读 · 开源资料</p>

</div>

<div class="section-heading" markdown="1">

## 当前研究方向

放牧机器人：研究机器人如何引导羊群到达目标区域。

</div>

<div class="research-feature" markdown="1">

<span class="eyebrow">放牧机器人</span>

### 放牧机器人研究

围绕羊群行为建模、仿真环境、放牧策略与机器人控制，整理研究思路、相关方法和实验记录。

[查看研究问题与实验路线 →](herding/index.md)

</div>

## 学习笔记 {#learning-notes}

第一次接触这些内容，先选一个目标，沿对应路线学习。每篇先读“要解决什么问题”，再跟图和小例子走完一遍；能说清输入、步骤、结果之后，再看完整程序和扩展内容。

| 想先学什么 | 从哪里开始 | 第一遍的小目标 |
| --- | --- | --- |
| 从零学习 C++ | [保存并编译第一个程序](programming/cpp/setup.md) → [变量与循环](programming/cpp/basics.md) → [函数与引用](programming/cpp/functions.md) | 能预测三个距离经过判断后，计数为什么是 1 |
| 看懂强化学习代码 | [Python 阅读入门](programming/python-reading.md) → [强化学习第一课](rl/start.md) → [TD 的代码](rl/code/td.md) | 找出环境给的奖励、算法的旧预测、这次更新的目标 |
| 理解深度算法怎样学习 | [公共符号](rl/math/index.md) → [网络与梯度](rl/network-basics.md) → [DQN](rl/intuition/dqn.md) | 用纸笔计算一次预测、损失和参数更新 |
| 了解放牧机器人任务 | [放牧研究概览](herding/index.md) → [坐标与控制](robotics/index.md) → [视觉输入](vision/index.md) | 画出机器人、羊群和目标区，说明单位、方向和成功条件 |

Python 和 C++ 是两条编程路线。阅读本站的 RL 代码从 Python 开始即可；C++ 路线则从基础语法逐步走到现代 C++ 与多文件项目。强化学习每种算法都有直觉、公式和代码三部分，可以围绕同一种算法来回对照。

### 每读完一小段，先检查这三件事

1. **能复述**：用自己的话说清它在解决哪个问题，例如“只数距离超过 3 米的羊”。
2. **能推演**：先遮住结果，按步骤写下变量或公式中间值，再对照预期输出。
3. **能解释一个改动**：只改一个条件，例如把“超过”换成“大于等于”，说明结果为什么变化。

练习中的“完整文件”可以按标明的文件名保存；“修改片段”要先看放在哪个位置。先做完正文的最小例子，再尝试扩展，不必一次把所有代码框拼在一起。

<div class="grid cards" markdown="1">

-   

    **强化学习**

    算法直觉、公式讲解与 Python 实践，涵盖基础价值方法、策略梯度和连续控制。

    [进入强化学习 →](rl/index.md)

-   

    **机器人技术**

    串联坐标系、仿真、导航和运动控制，建立从决策到执行的链路。

    [查看学习路线 →](robotics/index.md)

-   

    **计算机视觉**

    OpenCV、目标检测、图像分割、目标跟踪与相机标定。

    [查看感知路线 →](vision/index.md)

-   

    **智能放牧**

    明确任务边界、设计仿真环境，并用统一指标比较放牧策略。

    [进入研究专题 →](herding/index.md)

-   

    **编程技术**

    从 Python 代码阅读与第一个 C++ 程序开始，逐步学习函数、资源管理、现代 C++ 和 CMake。

    [查看实践清单 →](programming/index.md)

-   

    **论文阅读**

    用问题、方法、证据和局限整理文献，让阅读服务于实验设计。

    [使用阅读框架 →](papers/index.md)

</div>

<div class="resource-callout" markdown="1">

### 开源学习资料

收集机器人、计算机视觉等领域的教程与开源项目，作为日常学习的参考。

[浏览开源学习资料 →](opensource/index.md)

</div>

笔记持续整理与更新。
