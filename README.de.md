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
  Desktop-<b>parametrische CAD</b>-Plattform mit Fokus auf <b>historienbasierter Solid-Modellierung</b>, erweiterbaren Workbenches und einer Architektur in Industriequalität — angetrieben von <b>OpenCascade (OCCT)</b>.
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

## Was ist das?

**SolidDesigner** ist meine langfristige Produktlinie zum Aufbau einer CAD-Plattform der nächsten Generation:

- **History-based Modeling** mit Feature-Tree und deterministischer Regeneration
- **Workbenches** (Part / Assembly / Sketch / Drawing / Simulation / BIM-Erweiterungen) mit Ribbon-first UX
- Saubere Trennung der Schichten **Model / Representation / Display / Render / UI**, damit das System skalierbar bleibt

Wenn du einen pragmatischen „Industrial Software“-Ansatz für eine große CAD-Codebasis suchst (kein Spielzeug-Demo), ist das das Projekt.

## Kernfähigkeiten (High-Level)

- **Parametrische Feature-Modellierung**: Sketch → Feature-Erzeugung → Edit/Redefine → Regen
- **Kernel-Integration**: OCCT B-Rep Workflows (TopoDS / BRepBuilderAPI / Booleans / Fillet, …)
- **Professionelles UI-Framework**: Workbench-Switching, Ribbon, Docking-Panels, Multi-Document/MDI Layout
- **Dokument & Persistenz**: Container-Dokumentarchitektur (z. B. `.alice`), Versionierung/Upgrade-Pipeline Konzepte
- **Erweiterbarkeit**: Interface-getriebene Module, Plugin-fähige Runtime-Services

> Die genaue Feature-Abdeckung entwickelt sich schnell — das SolidDesigner-Repo ist die Quelle der Wahrheit.

## Start hier

- **Haupt-Repo:** https://github.com/hananiahhsu/SolidDesigner  
- **Sekundär:** OpenCAD (Experimente) — https://github.com/hananiahhsu/OpenCAD  
- **Domain-Erweiterungen:** SolidBIM / SolidSimulation / SolidRobot (je nach Verfügbarkeit)

</td>
<td valign="top" width="38%" align="center">
  <img
    src="assets/hero.png"
    width="100%" height="260"
    alt="SolidDesigner Vorschau"
  />
</td>
</tr>
</table>

---

## Architektur auf einen Blick

SolidDesigner folgt einer geschichteten Architektur, ausgelegt für langfristige Skalierung:

- **Core/Foundation**: Utilities, Math/Algorithmen, Plugin-/Event-Systeme
- **Geometry**: Kernel-Interfaces + OCCT Backend (und künftige Alternativen)
- **Data/Model**: Document, Object Store, Feature-Definitionen, Regen-Services
- **Representation/Display/Render**: RepGraph → DisplayPackages → RenderBackends
- **UI**: Qt/ADS Docking, Ribbon, Workbench-Lifecycle, Command-Routing

Die Struktur orientiert sich an Mustern reifer CAD-Systeme (Creo/NX/SolidWorks), bleibt aber pragmatisch für eine offene Codebasis.

---

## Roadmap-Richtung (öffentlich)

- **Feature-System Reifegrad**: stärkere Schemas, robuste Redefinition, History-Edits, Regen-Trace
- **TopoNaming/Selection-Stabilität**: stabile Referenzen bei Feature-Änderungen
- **Assemblies**: Constraints/Mates, Performance für große Baugruppen, Lightweight Reps
- **Drawings**: View-Generierung, Hidden-Line Removal, Bemaßung/Annotationen
- **Interoperabilität**: STEP/IGES/STL Pipelines (parallel zur Stabilisierung)
- **CAE/CAM Hooks**: Mesh/Analysis Views und Fertigungs-orientierte Workflows

---

## Mitmachen

- Bugs / Feature-Requests: https://github.com/hananiahhsu/SolidDesigner/issues  
- Design-Diskussionen: https://github.com/hananiahhsu/SolidDesigner/discussions  

Wenn du CAD/CAE/BIM-Infrastruktur baust und kollaborieren willst (Architektur, Kernel-Integration, UI, Storage/Versioning), eröffne ein Issue oder starte eine Diskussion.

---

<details>
  <summary><b>Developer-Stats (optional)</b></summary>

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

## Hinweise

- README.md (Englisch) ist die Referenz; Übersetzungen können hinterherhinken.
- Diese Seite ist ein Produkt-Überblick; detaillierte Build-Anleitung steht im **SolidDesigner** Repository.
