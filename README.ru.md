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
  Настольная <b>параметрическая CAD</b>-платформа, сфокусированная на <b>истории построений</b> (history-based solid modeling), расширяемых workbench’ах и архитектуре коммерческого уровня — на базе <b>OpenCascade (OCCT)</b>.
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

## Что это такое

**SolidDesigner** — моя долгосрочная продуктовая линия по созданию CAD-платформы нового поколения:

- **History-based моделирование** с деревом фич и детерминированной регенерацией
- **Workbench’и** (Part / Assembly / Sketch / Drawing / Simulation / BIM-расширения) с UX, ориентированным на Ribbon
- Чёткое разделение слоёв **Model / Representation / Display / Render / UI**, чтобы система масштабировалась

Если вам интересен практичный подход к «индустриальному» CAD-коду (не игрушечный демо-проект), это оно.

## Ключевые возможности (высокоуровнево)

- **Параметрическое feature-моделирование**: эскиз → создание фичи → редактирование/переопределение → regen
- **Интеграция геометрического ядра**: OCCT B-Rep (TopoDS / BRepBuilderAPI / булевы операции / филеты и т. п.)
- **Профессиональный UI**: переключение workbench’ей, Ribbon, док-панели, multi-document/MDI
- **Документы и хранение**: контейнерная архитектура (например, `.alice`), идеи версионирования/upgrade pipeline
- **Расширяемость**: интерфейсно-ориентированные модули, runtime-сервисы, готовые к плагинам

> Полное покрытие функциональности быстро меняется — ориентируйтесь на репозиторий SolidDesigner.

## С чего начать

- **Основной репозиторий:** https://github.com/hananiahhsu/SolidDesigner  
- **Дополнительно:** OpenCAD (эксперименты) — https://github.com/hananiahhsu/OpenCAD  
- **Доменные расширения:** SolidBIM / SolidSimulation / SolidRobot (по доступности)

</td>
<td valign="top" width="38%" align="center">
  <img
    src="assets/hero.png"
    width="100%" height="260"
    alt="Превью SolidDesigner"
  />
</td>
</tr>
</table>

---

## Архитектура в двух словах

SolidDesigner использует слоистую архитектуру для развития в крупном масштабе:

- **Core/Foundation**: утилиты, математика/алгоритмы, plugin/event системы
- **Geometry**: интерфейсы ядра + OCCT backend (и будущие альтернативы)
- **Data/Model**: документ, object store, определения фич, сервисы регенерации
- **Representation/Display/Render**: rep graph → display packages → render backends
- **UI**: Qt/ADS docking, Ribbon, жизненный цикл workbench’ей, маршрутизация команд

Структура опирается на паттерны зрелых CAD-систем (Creo/NX/SolidWorks), но остаётся прагматичной для открытого кода.

---

## Направление roadmap (публично)

- **Зрелость feature-системы**: более сильные схемы, надёжное переопределение, правки истории, regen trace
- **TopoNaming/стабильность выбора**: стабильные ссылки при редактировании фич
- **Сборки (Assemblies)**: constraints/mates, производительность больших сборок, lightweight reps
- **Чертежи (Drawings)**: генерация видов, hidden line removal, размеры/аннотации
- **Интероперабельность**: STEP/IGES/STL пайплайны (по мере стабилизации)
- **CAE/CAM hooks**: mesh/analysis views и производственно-ориентированные workflow

---

## Как участвовать

- Баги / запросы фич: https://github.com/hananiahhsu/SolidDesigner/issues  
- Дискуссии по дизайну: https://github.com/hananiahhsu/SolidDesigner/discussions  

Если вы строите CAD/CAE/BIM-инфраструктуру и хотите сотрудничать (архитектура, интеграция ядра, UI, storage/versioning), откройте issue или начните discussion.

---

<details>
  <summary><b>Статистика разработчика (опционально)</b></summary>

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

## Примечания

- Английская версия (README.md) — основная; переводы могут отставать.
- Эта страница — обзор продукта; подробные инструкции по сборке находятся в репозитории **SolidDesigner**.
