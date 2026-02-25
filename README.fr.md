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
  Plateforme CAD <b>paramétrique</b> pour poste de travail, axée sur la <b>modélisation solide à historique</b>, des workbenches extensibles et une architecture de niveau industriel — propulsée par <b>OpenCascade (OCCT)</b>.
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

## Qu’est-ce que c’est

**SolidDesigner** est ma ligne de produit à long terme pour construire une plateforme CAD de nouvelle génération :

- **Modélisation à historique** avec arbre de fonctions et régénération déterministe
- **Workbenches** (Part / Assembly / Sketch / Drawing / Simulation / extensions BIM) avec une UX centrée sur le Ribbon
- Séparation nette des couches **Model / Representation / Display / Render / UI** pour garder le système scalable

Si vous cherchez une approche pragmatique et « industrial software » d’un gros codebase CAD (pas une démo jouet), c’est ce projet.

## Capacités clés (haut niveau)

- **Modélisation paramétrique par fonctions** : esquisse → création de fonction → édition/redéfinition → regen
- **Intégration du noyau géométrique** : workflows OCCT B-Rep (TopoDS / BRepBuilderAPI / booléens / congés, etc.)
- **UI professionnelle** : workbench switching, Ribbon, panneaux dockables, disposition multi-doc/MDI
- **Document & persistance** : architecture de document conteneur (ex. `.alice`), notions de versioning/upgrade pipeline
- **Extensibilité** : modules orientés interfaces, services runtime prêts pour plugins

> La couverture exacte des fonctionnalités évolue rapidement — le dépôt SolidDesigner fait foi.

## Commencez ici

- **Dépôt principal :** https://github.com/hananiahhsu/SolidDesigner  
- **Secondaire :** OpenCAD (expérimentations) — https://github.com/hananiahhsu/OpenCAD  
- **Extensions métier :** SolidBIM / SolidSimulation / SolidRobot (selon disponibilité)

</td>
<td valign="top" width="38%" align="center">
  <img
    src="assets/hero.png"
    width="100%" height="260"
    alt="Aperçu SolidDesigner"
  />
</td>
</tr>
</table>

---

## Architecture en un coup d’œil

SolidDesigner suit une architecture en couches, conçue pour évoluer à grande échelle :

- **Core/Foundation** : utilitaires, maths/algorithmes, systèmes plugin/événements
- **Geometry** : interfaces noyau + backend OCCT (et alternatives futures)
- **Data/Model** : document, object store, définitions de fonctions, services de regen
- **Representation/Display/Render** : rep graph → display packages → backends de rendu
- **UI** : docking Qt/ADS, Ribbon, cycle de vie des workbenches, routage des commandes

Cette structure s’inspire des patterns des CAD matures (Creo/NX/SolidWorks), tout en restant pragmatique pour un codebase ouvert.

---

## Orientation de la roadmap (publique)

- **Maturité du système de fonctions** : schémas plus robustes, redéfinition solide, éditions d’historique, regen trace
- **TopoNaming / stabilité de sélection** : références stables lors des éditions
- **Assemblies** : contraintes/mates, performance grandes assemblées, représentations légères
- **Drawings** : génération de vues, hidden line removal, cotes/annotations
- **Interopérabilité** : pipelines STEP/IGES/STL (au rythme de la stabilisation)
- **Accroches CAE/CAM** : vues maillage/analyses et workflows orientés fabrication

---

## Participer

- Signaler un bug / demander une feature : https://github.com/hananiahhsu/SolidDesigner/issues  
- Discussions de conception : https://github.com/hananiahhsu/SolidDesigner/discussions  

Si vous construisez de l’infrastructure CAD/CAE/BIM et souhaitez collaborer (architecture, intégration noyau, UI, stockage/versioning), ouvrez une issue ou lancez une discussion.

---

<details>
  <summary><b>Statistiques développeur (optionnel)</b></summary>

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

- La version anglaise (README.md) est la référence ; les traductions peuvent prendre du retard.
- Cette page est un aperçu produit ; les instructions de build détaillées vivent dans le dépôt **SolidDesigner**.
