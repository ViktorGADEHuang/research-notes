# research-notes
个人科研与技术学习笔记。当前研究方向为放牧机器人。

## 本地环境的用途

`.venv` 仅用于预览和构建 MkDocs 网站。强化学习示例以带中文注释的学习代码形式提供，阅读教程无需安装算法依赖或创建额外的 RL 环境。网站不会自动执行 Python 或 C++ 示例。

编程技术中提供 C++17/20/23 教程与带注释的代码；强化学习提供算法直觉、公式与代码三个部分。各教程配有知识图、流程图或对比图。

机器人技术提供 14 章入门教程：位置与时间、传感器、坐标、运动学、反馈控制、ROS 2、tf2、URDF、MuJoCo、定位、规划、四足任务与闭环小项目。数值例子与机器人软件接口示例分别说明前置条件，阅读不要求在网站环境中安装 ROS 2 或 MuJoCo。

计算机视觉现在是一套独立的 14 章基础课程：像素、数组、颜色、插值、滤波、区域、特征、相机、网络、检测、跟踪、评估、小项目与放牧应用。各章按图解直觉、公式算例、中文注释代码和练习组织，核心例子仅用 Python 标准库；不安装模型、不训练，也不新增环境。

“开源资料教程”单独收纳具体项目。rm.cv.fans 源码阅读课位于 `docs/opensource/rm-cv-fans/`，共 14 课、15 张图解、17 个独立 C++ 程序，重点解释语法与通用视觉方法。原 `vision/rm-cv-fans/` 的 15 个页面地址构建时自动生成跳转，保留查询参数与锚点。源码事实、独立例子和 API 阅读片段分别说明，不构建原工程或展开专用火控实现。

## 本地预览

在项目目录打开终端，使用现有网站虚拟环境：

```
.\.venv\Scripts\python.exe -m mkdocs serve
```

## 发布前检查

```powershell
.\.venv\Scripts\python.exe -m mkdocs build --strict
.\.venv\Scripts\python.exe scripts/check_tutorials.py
.\.venv\Scripts\python.exe scripts/check_vision_examples.py
```

检查覆盖站内链接与锚点、代码围栏、Python 静态语法、URDF/MJCF 完整模型的 XML 结构、网页示例与本地源码一致性，并逐块对照教程中的代码、命令和预期输出是否完整显示，不运行 RL 示例。GitHub 自动发布也执行这些检查；失败时停止发布。自动检查不能替代概念审阅与浏览器显示检查。

视觉算例检查仅运行视觉课程里标为“独立教学示例”的 14 份标准库小程序，核对输出及小项目的时间、空数据和坐标边界；不会导入或运行 NumPy、OpenCV、RL 或原开源工程。临时文件只保存在 `.cache`，不进入网站。

教程代码在网页正文中展示。examples/cpp 与 examples/rl 仅供本地维护与静态检查，不参与网站发布；网站不提供示例下载入口或代码压缩包。

rm.cv.fans 阅读课的独立 C++ 例子另有维护检查：在已经安装 `g++` 并配置 PATH 时，执行 `.\.venv\Scripts\python.exe scripts/check_rmcv_examples.py`。编译器不在 PATH 时，用 `--compiler` 指定现有 `g++.exe` 的路径；检查会编译并运行本站独立例子和练习，核对页面预期输出，生成文件仅放在 `.cache`。它不会构建或运行原仓库，也不会运行 RL。
