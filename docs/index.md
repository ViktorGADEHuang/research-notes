---
title: 首页
hide:
  - navigation
  - toc
---

<div class="research-hero home-hero" markdown="1">
<div class="hero-copy" markdown="1">

<p class="hero-kicker">VIKTOR / RESEARCH NOTEBOOK</p>

# Viktor’s Research Notes

科研记录与技术学习笔记。

目前的研究方向是 **放牧机器人**。从机器人、强化学习、现代 C++ 与视觉的基础问题开始，配合图解、算例和注释代码逐步学习。

<div class="hero-actions" markdown="1">

[选择学习路线 ↓](#learning-notes){ .hero-btn .hero-btn-primary }
[放牧机器人研究 →](herding/index.md){ .hero-btn .hero-btn-outline }

</div>

<p class="hero-bottom">先理解问题，再推演数字，最后对照代码。</p>

</div>
<div class="hero-course" markdown="1">

<p class="hero-course-label">从零开始 · 推荐路线</p>
<p class="hero-course-title">机器人技术入门</p>
<p class="hero-course-description">从“我在哪里”，到读懂一个反馈闭环。</p>

<ol class="hero-course-steps">
  <li><span>01—04</span>认识机器人、观测与坐标</li>
  <li><span>05—06</span>理解运动与反馈控制</li>
  <li><span>07—10</span>读懂通信、结构与仿真</li>
  <li><span>11—14</span>连接定位、规划与任务</li>
</ol>

[从第 01 课开始 →](robotics/start.md){ .hero-course-link }

</div>
</div>

<div class="learning-metrics" aria-label="主要教程内容">
  <div><strong>14<span>章</span></strong><p>机器人基础与实践</p></div>
  <div><strong>12<span>种</span></strong><p>强化学习算法</p></div>
  <div><strong>15<span>章</span></strong><p>C++ 与现代 C++</p></div>
  <div><strong>14<span>章</span></strong><p>计算机视觉基础</p></div>
</div>

<div class="section-heading" markdown="1">

## 选一条路线，先完成一个小目标 {#learning-notes}

不必先学会所有工具。选一个你现在关心的问题，从第一步读起。

</div>

<div class="grid cards start-paths" markdown="1">

-   <span class="card-number">01 / 机器人技术</span>

    **机器人怎样知道自己在哪儿？**

    从位置、时间与传感器出发，理解坐标变换，再把运动、控制和软件连接起来。

    <span class="path-goal">第一个小目标：分清目标、观测和指令。</span>

    [从机器人第一课开始 →](robotics/start.md)

-   <span class="card-number">02 / 强化学习</span>

    **算法怎样根据结果调整判断？**

    先用走廊里的几步经历认识奖励与回报，再对照算法直觉、公式和 Python 代码。

    <span class="path-goal">第一个小目标：手算一次价值更新。</span>

    [从强化学习第一课开始 →](rl/start.md)

-   <span class="card-number">03 / C++ 与现代 C++</span>

    **代码写在哪里，怎样得到结果？**

    从保存和编译第一个程序开始，逐步理解函数、容器、资源管理和多文件项目。

    <span class="path-goal">第一个小目标：显示自己写的一行文字。</span>

    [从第一个 C++ 程序开始 →](programming/cpp/setup.md)

-   <span class="card-number">04 / 计算机视觉</span>

    **一张图，怎样变成有含义的数字？**

    从像素、颜色与数组开始，再理解滤波、相机、检测、跟踪和评估。

    <span class="path-goal">第一个小目标：找到一个像素，并解释它的坐标。</span>

    [从视觉第一课开始 →](vision/images.md)

</div>

## 浏览全部专题

<div class="grid cards topic-cards" markdown="1">

-   **机器人技术**

    位置、传感器、坐标、控制、ROS 2、仿真与导航。

    [查看 14 章学习路线 →](robotics/index.md)

-   **强化学习**

    价值方法、策略梯度与连续控制，分直觉、公式、代码阅读。

    [进入算法目录 →](rl/index.md)

-   **编程技术**

    Python 代码阅读、C++17/20/23、CMake 与数据处理。

    [选择编程路线 →](programming/index.md)

-   **计算机视觉**

    14 章独立基础课，配图解、手算、中文注释和自测练习。

    [查看视觉学习路线 →](vision/index.md)

-   **智能放牧**

    梳理研究问题、羊群状态、机器人动作和实验指标。

    [进入放牧研究专题 →](herding/index.md)

-   **论文阅读**

    用问题、方法、证据和局限整理阅读记录。

    [查看论文阅读方法 →](papers/index.md)

</div>

<div class="learning-method" markdown="1">

### 一篇教程，可以分三次读

**先说清问题**：输入是什么，想得到什么结果。**再推一次数字**：遮住答案，写下中间步骤。**最后改一个条件**：说明输出为什么改变。

遇到代码先看它是“完整文件”还是“局部片段”，再按文字说明对照。Python 阅读入门可以随时查阅，阅读强化学习示例不需要创建 RL 环境。

[查阅 Python 阅读入门 →](programming/python-reading.md) · [开源项目配套教程 →](opensource/tutorials/index.md) · [浏览开源学习资料 →](opensource/index.md)

</div>
