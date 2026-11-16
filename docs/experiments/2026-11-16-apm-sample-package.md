# APM サンプルパッケージの導入

## 状態

採用

## 目的と仮説

- 解決したい問題: 初期化だけの APM プロジェクトに、Copilot で利用できる指示・プロンプト・エージェント・スキルを追加する。
- 検証可能な仮説: バージョン指定した公式サンプルパッケージを APM で導入すれば、依存関係と展開ファイルをロックし、再検査できる。
- 対象範囲: `apm.yml`、`apm.lock.yaml`、Copilot 向けに展開されるサンプルと推移依存、README の利用手順。
- 今回やらないこと: パッケージの内容のカスタマイズ、依存関係の更新、APM CI ワークフローの追加。

## 成功条件

- [x] APM プロジェクトを Copilot ターゲットで初期化する。
- [x] `microsoft/apm-sample-package#v1.0.0` と推移依存がロックされる。
- [x] Copilot 用ファイルが展開され、APM 監査でロックと展開の整合性が確認できる。
- [x] APM の再インストール・監査手順を README に記載する。

## 実装と検証の計画

1. 初期化前に既存の `.github/` 配下と選定パッケージの内容を確認する。
2. `apm init --yes --target copilot` とバージョン固定した `apm install` を実行する。
3. `apm audit --ci` と `make check` でロック・展開・リポジトリ設定を検証する。

## 結果

- 実行したコマンドと結果:
  - `apm init --yes --target copilot`: 成功。`apm.yml` を作成。
  - `apm install microsoft/apm-sample-package#v1.0.0 --target copilot`: 成功。サンプルと推移依存を導入。
  - `apm audit --ci`: 10 項目すべて成功、展開差分なし。組織ポリシーは見つからず、ポリシー適用はスキップされた。
  - `make check`: 成功。
- 成功条件の達成状況: すべて達成。Copilot 向けの指示、エージェント、2 つのプロンプト、2 つのスキルが展開された。
- 未検証事項: Dev Container 内での再インストール。今回の実行環境には Docker / Dev Containers CLI がなく、APM CLI は一時領域に導入して検証した。
- 採用 / 不採用の判断と理由: 採用。サンプルと推移依存の内容を確認し、`apm.lock.yaml` に実際のコミットが固定された。
- 再現方法と次の課題: コンテナを再ビルドし、リポジトリのルートで `apm install` と `apm audit --ci` を実行する。推移依存の参照は上流で未固定のため、更新時は解決コミットの変更をレビューする。
