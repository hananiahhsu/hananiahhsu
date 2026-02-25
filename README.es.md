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
  Plataforma CAD <b>paramétrica</b> de escritorio, centrada en <b>modelado sólido con historial</b>, workbenches extensibles y una arquitectura de nivel comercial — impulsada por <b>OpenCascade (OCCT)</b>.
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

## Qué es

**SolidDesigner** es mi línea de producto a largo plazo para construir una plataforma CAD de próxima generación:

- **Modelado basado en historial** con árbol de features y regeneración determinista
- **Workbenches** (Part / Assembly / Sketch / Drawing / Simulation / extensiones BIM) con UX “Ribbon-first”
- Separación limpia de capas **Model / Representation / Display / Render / UI** para escalar sin colapsar

Si buscas un enfoque práctico y de “software industrial” para un codebase CAD grande (no un demo juguete), este es el proyecto.

## Capacidades clave (alto nivel)

- **Modelado paramétrico por features**: sketch → creación de feature → editar/redefinir → regen
- **Integración del kernel geométrico**: workflows OCCT B-Rep (TopoDS / BRepBuilderAPI / booleanas / fillet, etc.)
- **UI profesional**: cambio de workbench, Ribbon, paneles acoplables, layout multi-documento/MDI
- **Documento y persistencia**: arquitectura de contenedor (p. ej. `.alice`), conceptos de versionado/upgrade pipeline
- **Extensibilidad**: módulos guiados por interfaces, servicios runtime listos para plugins

> La cobertura exacta de features evoluciona rápido — el repo de SolidDesigner es la fuente de verdad.

## Empieza aquí

- **Repo principal:** https://github.com/hananiahhsu/SolidDesigner  
- **Secundario:** OpenCAD (experimentos) — https://github.com/hananiahhsu/OpenCAD  
- **Extensiones de dominio:** SolidBIM / SolidSimulation / SolidRobot (según disponibilidad)

</td>
<td valign="top" width="38%" align="center">
  <img
    src="assets/hero.png"
    width="100%" height="260"
    alt="Vista previa de SolidDesigner"
  />
</td>
</tr>
</table>

---

## Arquitectura de un vistazo

SolidDesigner sigue una arquitectura por capas pensada para evolucionar a gran escala:

- **Core/Foundation**: utilidades, matemáticas/algoritmos, sistemas de plugins/eventos
- **Geometry**: interfaces del kernel + backend OCCT (y futuras alternativas)
- **Data/Model**: documento, object store, definiciones de features, servicios de regeneración
- **Representation/Display/Render**: rep graph → display packages → backends de render
- **UI**: docking Qt/ADS, Ribbon, ciclo de vida de workbenches, enrutamiento de comandos

La estructura se inspira en patrones de CAD maduros (Creo/NX/SolidWorks), manteniéndose pragmática para un codebase abierto.

---

## Dirección del roadmap (público)

- **Madurez del sistema de features**: esquemas más fuertes, redefinición robusta, ediciones de historial, regen trace
- **TopoNaming/estabilidad de selección**: referencias estables tras editar features
- **Ensamblajes**: constraints/mates, rendimiento en grandes ensamblajes, representaciones ligeras
- **Planos**: generación de vistas, hidden line removal, cotas/anotaciones
- **Interoperabilidad**: pipelines STEP/IGES/STL (a medida que se estabilizan)
- **Hooks CAE/CAM**: vistas de malla/análisis y flujos orientados a fabricación

---

## Participa

- Reportar bugs / pedir features: https://github.com/hananiahhsu/SolidDesigner/issues  
- Discusiones de diseño: https://github.com/hananiahhsu/SolidDesigner/discussions  

Si estás construyendo infraestructura CAD/CAE/BIM y quieres colaborar (arquitectura, integración del kernel, UI, storage/versioning), abre un issue o inicia una discusión.

---

<details>
  <summary><b>Estadísticas de desarrollador (opcional)</b></summary>

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

## Notas

- La versión en inglés (README.md) es la referencia; las traducciones pueden ir por detrás.
- Esta página es un resumen del producto; las instrucciones de build detalladas están en el repo **SolidDesigner**.
