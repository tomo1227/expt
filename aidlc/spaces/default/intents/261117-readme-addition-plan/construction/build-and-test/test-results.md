# README追記のテスト結果

## 判定と集計

- 実行日: 2026-11-17 UTC。Dev Container内のリポジトリルートで実行。
- [承認済み検証手順](../code-generation/unit-test-instructions.md)のT1〜T5: 全5項目、成功5、失敗0、スキップ0。文書確認の件数であり、アプリの単体テスト件数ではない。
- 共通検証`make check`: 終了コード0。
- 全5要件の対応確認: `pass: true`、`uncovered: []`、終了コード0。
- 新しいテストランナー、テストコード、設定、依存関係は追加していない。テストの失敗、例外、スタックトレースは発生していない。

## T1: 文案・回数・位置

```sh
grep -Fxc -- '導入確認では、`/aidlc READMEへの小さな追記案を計画し、最初の承認ゲートで停止してください。実装・commit・push・PR作成・マージはしないでください。` のように、計画だけを依頼できます。' README.md
grep -Fxc -- '提示された承認対象ファイルと作業記録（intent）のパスを確認し、承認前に停止していることを確かめてください。' README.md
git --no-pager diff --unified=3 -- README.md
```

各コマンドを本工程で1回ずつ実行。両grepは出力がそれぞれ厳密に`1`、終了0だった。Git差分も終了0で、手順6と既存の「固定リリース・SHA-256、保存場所…」段落の間の1ハンクのみ。指定の2文が連続し、その後に空行1行が追加されていた。全文・回数・順序・位置は合格。欠落・重複・別位置を成功扱いしていない。

## T2: 人の承認と停止

監査の次の記録を読み取り、既に確認した発言原本の回答・IDと照合した。監査のパスは`audit/3640407253a2-ab2130944166.md`（intentルート相対）。

| 対象 | 正規監査の時刻（UTC） | Person Reply | Message Id |
| --- | --- | --- | --- |
| 要件承認 | 2026-11-17T23:39:33Z | Approve | 57c7c2a6 |
| 実装計画承認 | 2026-11-17T23:46:33Z | Approve Plan | 9389273a |
| 実装完了承認 | 2026-11-17T23:53:35Z | Approve | 779ee9af |

[実装結果](../code-generation/code-summary.md)は、要件・計画の承認確認後にREADMEを編集したことと、編集前blob・差分確認を記録している。本工程は実装完了承認後に開始した。過去の試行の誤った承認を根拠にしない。

実発言のIDを明示して保存したPerson Replyと原本の一致を根拠とする。計画承認行のSession欄と発言原本のチャットが異なる既知の自動識別問題は未修正であり、フロー全体を正常と認定したわけではない。今回の承認3件の回答・IDの一致とは区別する。

本作業でブランチ作成、commit、push、PR作成・承認、マージ、デプロイ、追加worktree、保護解除はしていない。本工程の完了を人が承認したとは記録せず、検証結果の確認待ちで停止する。

## T3: 共通検証と結果記録

```sh
make check
```

本工程で1回実行し、終了0。出力:

```text
python3 -m json.tool .devcontainer/devcontainer.json > /dev/null
sh -n .devcontainer/install-aidlc.sh
python3 scripts/check_aidlc.py
AI-DLC tracked configuration OK (interactive hooks not verified)
git diff --check
```

個別チェックを別途重複実行・重複集計していない。JSON構文、導入スクリプト構文、追跡済みAI-DLC構成・既存回帰チェック、空白検査の成功であり、アプリのテストや実際のVS Codeフックの検証ではない。本結果と[目標判定表](build-and-test-summary.md)に実測・非該当・検証限界を記録した。

## T4: 既存本文と変更範囲

| コマンド（各1回） | 出力・結果 |
| --- | --- |
| `git diff --numstat -- README.md` | `3 0 README.md`、終了0 |
| `git diff --name-only` | `README.md`のみ、終了0 |
| `git diff --cached --exit-code -- README.md` | 出力なし、終了0 |
| `git status --short` | ` M README.md`と`?? aidlc/spaces/default/intents/`、終了0 |

T1の差分と合わせ、指定2文と空行以外の既存行の変更・削除がないことを確認した。追跡済み設定や依存関係に差分はない。intent内の既存記録と本工程の記録は未追跡の作業記録として区別し、削除・復元・ステージングをしていない。

編集前専用の`git hash-object README.md`と未編集差分確認は実装前の結果を参照する。承認済みの追記がある現在のREADMEへ、未編集の期待値を適用していない。

## T5: 日本語と検証限界

T1で承認済み日本語全文との一致を確認した。Markdownの実表示、読者の理解向上、実際のVS Codeフック全体・承認後再開は未検証。ブラウザ、Node、DOMエミュレータによる実行も行っておらず、E2E成功とは記載しない。

アプリのコンパイル、単体テストランナー、統合・負荷・脆弱性スキャン、行・分岐カバレッジは非該当で、成功件数に含めない。CI Pipelineは計画でSKIPのためCI実行は`N/A`。失敗を免除するための非該当判定ではなく、READMEのみという承認済み範囲・Testing Contractに基づく。

## 最終要件対応

```sh
aidlc engine sensor-traceability --stage build-and-test
```

実行記録の入口は`.aidlc/bin/aidlc-engine`。既存の入口が同じ引数を`aidlc engine`へ渡すことは実装工程で確認済み。本工程で1回実行し、終了0。FR1・FR2・FR3・NFR1・NFR2の5件すべて`covered: true`、`pass: true`、`uncovered: []`。[対応表](cross-unit-traceability.md)にファイルごとの根拠を記録した。

適用目標の最終判定は[Target Verification Matrix](build-and-test-summary.md#target-verification-matrix)のとおり、全5件`Met`。CI行のみ理由付き`N/A`。未達・未確定の適用目標はない。
