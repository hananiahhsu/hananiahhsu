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
  A desktop <b>parametric CAD</b> platform focused on <b>history-based solid modeling</b>, extensible workbenches, and a commercial-grade architecture — powered by <b>OpenCascade (OCCT)</b>.
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

## What it is

**SolidDesigner** is my long-term product line for building a next-generation CAD platform:
- **History-based modeling** with a feature tree and deterministic regeneration
- **Workbenches** (Part / Assembly / Sketch / Drawing / Simulation / BIM extensions) with a Ribbon-first UX
- A clean separation of **Model / Representation / Display / Render / UI** layers to keep the system scalable

If you are looking for a practical, “industrial software” approach to a large CAD codebase (not a toy demo), this is the project.

## Key capabilities (high level)

- **Parametric feature modeling**: sketch → feature creation → edit/redefine → regen
- **Geometry kernel integration**: OCCT B-Rep workflows (TopoDS / BRepBuilderAPI / Boolean / fillet, etc.)
- **Professional UI framework**: workbench switching, Ribbon, dockable panels, multi-document/MDI layout
- **Document & persistence**: container-based document architecture (e.g., `.alice`), versioning/upgrade pipeline concepts
- **Extensibility**: interface-driven modules, plugin-ready runtime services

> Exact feature coverage evolves quickly — please treat the SolidDesigner repo as the source of truth.

## Start here

- **Main repo:** https://github.com/hananiahhsu/SolidDesigner  
- **Secondary:** OpenCAD (experiments) — https://github.com/hananiahhsu/OpenCAD  
- **Domain extensions:** SolidBIM / SolidSimulation / SolidRobot (as available)

</td>
<td valign="top" width="38%" align="center">
  <img
    src="assets/hero.png"
    width="100%" height="260"
    alt="SolidDesigner preview"
  />
</td>
</tr>
</table>

---

## Architecture at a glance

SolidDesigner follows a layered architecture designed for large-scale evolution:

- **Core/Foundation**: utilities, math/algorithms, plugin/event systems
- **Geometry**: kernel interfaces + OCCT backend (and future alternatives)
- **Data/Model**: document, object store, feature definitions, regen services
- **Representation/Display/Render**: rep graph → display packages → render backends
- **UI**: Qt/ADS-based docking, Ribbon, workbench lifecycle, command routing

This structure is intentionally similar to how mature CAD systems scale (Creo/NX/SolidWorks-class patterns), while still being pragmatic for an open codebase.

---

## Roadmap direction (public)

- **Feature system maturity**: stronger schemas, robust redefine, history edits, regen trace
- **TopoNaming/selection stability**: stable references across feature edits
- **Assemblies**: constraints/mates, large-assembly performance, lightweight reps
- **Drawings**: view generation, hidden line removal, dimensions/annotations
- **Interoperability**: STEP/IGES/STL pipelines (as features stabilize)
- **CAE/CAM hooks**: mesh/analysis views and manufacturing-oriented workflows

---

## Get involved

- Report bugs / request features: https://github.com/hananiahhsu/SolidDesigner/issues  
- Design discussions: https://github.com/hananiahhsu/SolidDesigner/discussions  

If you’re building CAD/CAE/BIM infrastructure and want to collaborate (architecture, kernel integration, UI systems, storage/versioning), open an issue or start a discussion.

---

<details>
  <summary><b>Developer stats (optional)</b></summary>

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

## Notes

- The English README is the canonical reference. Translations may lag behind.
- This profile page is a product overview; detailed build instructions live in the **SolidDesigner** repository.
