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
  <b>履歴ベースのソリッドモデリング</b>／拡張可能なWorkbench／商用グレードのアーキテクチャに焦点を当てた、デスクトップ<b>パラメトリックCAD</b>プラットフォーム — <b>OpenCascade (OCCT)</b> により駆動。
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

## これは何か

**SolidDesigner** は、次世代CADプラットフォームを長期的に構築するためのプロダクトラインです。

- **履歴ベースのモデリング**：フィーチャーツリーと決定的な再生成（regen）
- **Workbench**（Part / Assembly / Sketch / Drawing / Simulation / BIM 拡張）と Ribbon中心UX
- **Model / Representation / Display / Render / UI** の分離により、大規模開発でも破綻しにくい構造

「おもちゃのデモ」ではなく、実用的な“産業用ソフトウェア”の作り方を目指しています。

## 主な能力（概要）

- **パラメトリック・フィーチャーモデリング**：スケッチ → フィーチャ作成 → 編集/再定義 → 再生成
- **ジオメトリカーネル統合**：OCCT B-Rep（TopoDS / BRepBuilderAPI / Boolean / Fillet など）
- **プロ向けUI基盤**：Workbench切替、Ribbon、ドッキングパネル、MDIレイアウト
- **ドキュメント/永続化**：コンテナ型ドキュメント（例：`.alice`）とバージョン/アップグレードの考え方
- **拡張性**：インタフェース駆動のモジュール、プラグイン前提のランタイム

> フィーチャの網羅度は高速に進化します。最新状況は SolidDesigner リポジトリを参照してください。

## まずはこちら

- **メイン：** https://github.com/hananiahhsu/SolidDesigner  
- **サブ：** OpenCAD（実験）— https://github.com/hananiahhsu/OpenCAD  
- **拡張ドメイン：** SolidBIM / SolidSimulation / SolidRobot（公開されている範囲で）

</td>
<td valign="top" width="38%" align="center">
  <img
    src="assets/hero.png"
    width="100%" height="260"
    alt="SolidDesigner プレビュー"
  />
</td>
</tr>
</table>

---

## アーキテクチャ概要

SolidDesigner は、大規模進化を前提にしたレイヤードアーキテクチャを採用します：

- **Core/Foundation**：ユーティリティ、数学/アルゴリズム、プラグイン/イベント
- **Geometry**：カーネルIF + OCCTバックエンド（将来的に代替も想定）
- **Data/Model**：ドキュメント、オブジェクトストア、フィーチャ定義、再生成サービス
- **Representation/Display/Render**：RepGraph → DisplayPackage → RenderBackend
- **UI**：Qt/ADSドッキング、Ribbon、Workbenchライフサイクル、コマンドルーティング

成熟したCAD（Creo/NX/SolidWorks級）がスケールする際のパターンを参考にしつつ、オープンなコードベースとして現実的に構成しています。

---

## ロードマップ（方向性）

- **フィーチャシステム成熟**：スキーマ強化、堅牢な再定義、履歴編集、regen trace
- **TopoNaming/選択安定**：編集後も参照が壊れにくい安定参照
- **アセンブリ**：拘束/メイト、LAA性能、軽量表現
- **図面**：ビュー生成、隠線処理、寸法/注記
- **相互運用**：STEP/IGES/STL パイプライン（安定化に合わせて）
- **CAE/CAM フック**：メッシュ/解析ビュー、製造指向ワークフロー

---

## 参加/コラボ

- バグ報告・要望： https://github.com/hananiahhsu/SolidDesigner/issues  
- 設計ディスカッション： https://github.com/hananiahhsu/SolidDesigner/discussions  

CAD/CAE/BIM基盤（アーキテクチャ、カーネル統合、UI、ストレージ/バージョニング）で協業したい方は Issue または Discussion からどうぞ。

---

<details>
  <summary><b>開発者統計（任意）</b></summary>

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

## 注意

- 英語版（README.md）が参照元（最新版）です。翻訳は遅れる場合があります。
- このページはプロダクト概要です。詳細なビルド手順は **SolidDesigner** リポジトリにあります。
