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

第一次接触这些内容，可以从一个小问题开始。每篇先读例子和图，再顺着代码或数字推演，最后尝试自测；暂时不熟悉的高级部分可以留到第二遍。

| 想先学什么 | 从哪里开始 | 第一遍的小目标 |
| --- | --- | --- |
| 看懂一段程序 | [Python 阅读入门](programming/python-reading.md) / [第一个 C++ 程序](programming/cpp/setup.md) | 说出输入是什么，每一步改了哪个变量，最后输出什么 |
| 理解机器人怎样学习 | [强化学习第一课](rl/start.md) | 分清一次奖励、整局回报和对未来的估计 |
| 了解放牧任务 | [放牧研究概览](herding/index.md) | 画出机器人、羊群和目标区，写清怎样才算成功 |

下面按主题继续深入。强化学习每种算法都有直觉、公式和代码三部分；C++ 从基础语法逐步走到现代 C++ 与多文件项目。

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

    围绕科研代码组织、数据处理与机器人通信积累工程实践。

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
