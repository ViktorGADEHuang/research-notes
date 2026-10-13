# research-notes
个人科研与技术学习笔记。当前研究方向为放牧机器人。

## 本地环境的用途

`.venv` 仅用于预览和构建 MkDocs 网站。强化学习示例以带中文注释的学习代码形式提供，阅读教程无需安装算法依赖或创建额外的 RL 环境。网站不会自动执行 Python 或 C++ 示例。

编程技术中提供 C++17/20/23 教程与带注释的代码；强化学习提供算法直觉、公式与代码三个部分。各教程配有知识图、流程图或对比图。

## 本地预览

在项目目录打开终端，使用现有网站虚拟环境：

```
.\.venv\Scripts\python.exe -m mkdocs serve
```

## 发布前检查

```powershell
.\.venv\Scripts\python.exe -m mkdocs build --strict
.\.venv\Scripts\python.exe scripts/check_tutorials.py
```

检查覆盖站内链接与锚点、代码围栏、Python 静态语法、网页示例与本地源码一致性，并逐块对照教程中的代码、命令和预期输出是否完整显示，不运行 RL 示例。GitHub 自动发布也执行这些检查；失败时停止发布。自动检查不能替代概念审阅与浏览器显示检查。

教程代码在网页正文中展示。examples/cpp 与 examples/rl 仅供本地维护与静态检查，不参与网站发布；网站不提供示例下载入口或代码压缩包。
