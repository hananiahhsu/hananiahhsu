<p align="center">
  <a href="README.md">English</a> |
  <a href="README.zh.md">中文</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.fr.md">Français</a> |
  <a href="README.de.md">Deutsch</a> |
  <a href="README.es.md">Español</a> |
  <a href="README.ru.md">Русский</a>
</p>

<h1 align="center">SolidDesigner</h1>

<p align="center">
  面向<b>历史树驱动的实体建模</b>、可扩展 Workbench、以及商业级架构的桌面<b>参数化 CAD</b>平台 — 基于 <b>OpenCascade (OCCT)</b>。
</p>

<p align="center">
  <a href="https://github.com/hananiahhsu/SolidDesigner"><img alt="Repo" src="https://img.shields.io/badge/GitHub-SolidDesigner-181717?logo=github&logoColor=white"></a>
  <a href="https://github.com/hananiahhsu/SolidDesigner/issues"><img alt="Issues" src="https://img.shields.io/badge/Issues-Tracking-1F6FEB?logo=github&logoColor=white"></a>
  <a href="https://github.com/hananiahhsu/SolidDesigner/discussions"><img alt="Discussions" src="https://img.shields.io/badge/Discussions-Community-8957E5?logo=github&logoColor=white"></a>
</p>

<p align="center">
  <img alt="C++" src="https://img.shields.io/badge/C%2B%2B-00599C?logo=c%2B%2B&logoColor=white">
  <img alt="CMake" src="https://img.shields.io/badge/CMake-064F8C?logo=cmake&logoColor=white">
  <img alt="Qt" src="https://img.shields.io/badge/Qt-41CD52?logo=qt&logoColor=white">
  <img alt="OpenCascade" src="https://img.shields.io/badge/OCCT-OpenCascade-0B5FFF">
</p>

<table>
  <tr>
    <td valign="top" width="62%">

## 这是什么

**SolidDesigner** 是我长期投入的产品线，用来打造下一代 CAD 平台：

- **历史树特征建模**：特征树 + 确定性的再生（regen）
- **Workbench 体系**（Part / Assembly / Sketch / Drawing / Simulation / BIM 扩展），以 Ribbon 为核心交互
- **Model / Representation / Display / Render / UI** 分层清晰，支撑大型系统长期演进

如果你想看到一个“工业软件”思路下的大型 CAD 代码库（而不是玩具 Demo），这就是这个项目。

## 核心能力（高层概览）

- **参数化特征建模**：草图 → 特征创建 → 编辑/重定义 → 再生
- **几何内核集成**：OCCT B-Rep 工作流（TopoDS / BRepBuilderAPI / Boolean / Fillet 等）
- **专业 UI 框架**：Workbench 切换、Ribbon、Dock 面板、MDI/多文档布局
- **文档与持久化**：容器化文档架构（例如 `.alice`），版本化/升级流水线思想
- **可扩展性**：面向接口的模块化设计，运行时服务具备插件化基础

> 具体功能覆盖在快速演进中，请以 SolidDesigner 仓库为准。

## 从这里开始

- **主仓库：** https://github.com/hananiahhsu/SolidDesigner  
- **辅助/实验：** OpenCAD — https://github.com/hananiahhsu/OpenCAD  
- **领域扩展：** SolidBIM / SolidSimulation / SolidRobot（按公开情况）

</td>
<td valign="top" width="38%" align="center">
  <img
    src="assets/hero.png"
    width="100%" height="260"
    alt="SolidDesigner 预览"
  />
</td>
</tr>
</table>

---

## 架构一览

SolidDesigner 采用面向大规模演进的分层架构：

- **Core/Foundation**：工具库、数学/算法、插件/事件系统
- **Geometry**：Kernel Interface + OCCT 后端（未来可替换）
- **Data/Model**：文档、对象存储、特征定义、再生服务
- **Representation/Display/Render**：RepGraph → DisplayPackage → RenderBackend
- **UI**：Qt/ADS Docking、Ribbon、Workbench 生命周期、命令路由

整体结构参考成熟 CAD 系统（Creo/NX/SolidWorks）的可扩展模式，同时保持对开源代码库的可落地性。

---

## 路线方向（公开）

- **特征系统成熟**：更强的 Schema、更可靠的重定义、历史编辑、Regen Trace
- **TopoNaming / 选择稳定性**：特征编辑后引用更稳定
- **装配**：约束/配合、大装配性能、轻量表示
- **工程图**：视图生成、隐线处理、标注/注释
- **互操作**：STEP/IGES/STL 管线（随稳定性逐步推进）
- **CAE/CAM 挂钩**：网格/分析视图与面向制造的工作流

---

## 参与协作

- Bug / 需求： https://github.com/hananiahhsu/SolidDesigner/issues  
- 设计讨论： https://github.com/hananiahhsu/SolidDesigner/discussions  

如果你也在做 CAD/CAE/BIM 基础设施（架构、内核封装、UI、存储/版本化），欢迎开 Issue 或发起 Discussion 一起推进。

---

<details>
  <summary><b>开发者统计（可选）</b></summary>

  <p>
    <img
      src="assets/stats/metrics.svg"
      width="100%"
      alt="GitHub Metrics"
    />
  </p>

  <p>
    <img
      src="https://github-readme-activity-graph.vercel.app/graph?username=hananiahhsu&theme=github-compact&hide_border=true&area=false"
      width="100%"
      alt="Contribution Graph"
    />
  </p>
</details>

---

## 说明

- 英文版（README.md）是权威参考；翻译可能会有延迟。
- 这里是产品概览；详细构建/使用说明请以 **SolidDesigner** 仓库 README 为准。
