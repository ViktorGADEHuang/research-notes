# 开源学习资料：带着问题查原始来源

先用本站的图解建立概念，再到原始资料核对公式与接口。资料的用途不同，不必同时读完所有入口。

---


## 看图梳理

![资源要带着问题用](../assets/learning/opensource-index.svg){ .learning-figure }

[打开大图](../assets/learning/opensource-index.svg)

**先确定目标**：学理论还是读实现，环境与工具是否匹配；**查原始资料**：官方文档与论文，对照版本与接口；**形成自己的记录**：最小例子与笔记，保留来源与限制。


## 先按问题选择入口

| 你正在问什么 | 资料入口 | 建议怎么读 |
| --- | --- | --- |
| 强化学习算法的目标是什么？ | [Spinning Up](https://spinningup.openai.com/en/latest/spinningup/rl_intro2.html) | 先读关键方程，再把更新步骤与本站公式对照 |
| 库支持什么动作空间？ | [SB3 算法支持表](https://stable-baselines3.readthedocs.io/en/master/guide/algos.html) | 检查 Discrete / Box，再看对应算法参数；阅读即可 |
| C++ 的资源由谁负责？ | [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) | 带着所有权、生命周期的问题查条目 |
| 为什么像素不能直接当成米？ | [OpenCV 相机标定](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html) | 分清内参、外参、深度与坐标系 |
| 多文件程序怎样一起编译？ | [CMake 入门](https://cmake.org/cmake/help/latest/guide/tutorial/index.html) | 先理解目标、源文件、配置与构建四个词 |

官方文档可能展示比本教程更新的功能。核对版本、参数默认值和标准要求，不能只根据函数名称复制代码。

## 01 · 机器人学习

### Robotics Tutorial

**一套系统化的机器人学习教程**

涵盖机器人数学基础、C++、SLAM、运动规划与控制、足式机器人及具身智能等技术方向，适合机器人领域的系统学习。

**📖 主要学习方向**

- 机器人数学基础与运动学
- C++ 编程与机器人软件开发
- SLAM 定位与建图
- 机器人路径规划与运动控制
- 足式机器人与具身智能

**🔗 资料入口**

[🌐 GitHub 开源项目 — Robotics Tutorial](https://github.com/Michael-Jetson/Robotics_Tutorial)

[📖 在线阅读教程](https://robotics-tutorial-wiki.vercel.app/)

---

## 02 · 机器人视觉

### 浙江大学 RoboMaster 视觉组学习资料

**浙江大学 RoboMaster 机甲大师视觉组入组培训教程**

面向机器人视觉开发，包含基础编程、计算机视觉、相机标定、目标跟踪及机器人自瞄系统等学习内容。

**📖 主要学习方向**

- Linux 与机器人开发环境
- OpenCV 计算机视觉
- 工业相机与相机标定
- PnP 位姿解算
- Kalman 滤波与目标跟踪
- 神经网络与 YOLO

**🔗 资料入口**

[🌐 在线阅读 — 浙大 RoboMaster 视觉组培训教程](https://hello-world-vision.github.io/Vision_Website/induction-training/)

---

## 📝 学习记录

这些开源资料将作为个人学习与科研的参考资源，后续逐步整理相关知识点、算法原理、代码实践及实验总结。


*📌 声明：以上资料均来自公开项目，原始内容及版权归各项目作者所有。本页面仅用于学习资源整理与分享。*
