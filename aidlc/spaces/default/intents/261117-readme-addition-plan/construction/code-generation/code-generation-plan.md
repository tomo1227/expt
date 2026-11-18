# README追記の実装計画

## Summary

- Builds: 承認済みのREADME追記案2文を、指定位置へ1回だけ反映する。
- Touches: README.mdの1か所と、このintent内の実装計画・検証手順・結果記録のみ。
- Tests: FR1〜FR3・NFR1〜NFR2に対応する文書確認5項目とmake check。重複・位置不整合・既存本文変更を検出する。

## 根拠と仮説

[承認済み要件](../../inception/requirements-analysis/requirements.md)のStep 5〜8とAC6〜AC8を実施する。User Storiesは作成していないため、各手順を要件IDへ直接対応付ける。

仮説: 計画のみを依頼して承認前に停止する例を2文示すことで、既存の承認・公開ルールを変えずに導入確認の始め方を明確にできる。

この計画は未承認。要件への承認や旧実装計画の回答を、この計画の承認として使用しない。計画の承認まではREADMEを編集しない。

## 実装手順

- [x] Step 1（FR1・FR2・NFR1）: 現行の実装計画に対する人の承認を確認し、READMEの編集前状態と作業差分を確認する。基準blobは`7a48369934c7c1006489e99093ec221b403d9e8c`。READMEの内容が変わっている、追記が既にある、挿入位置が不明確、または承認を確認できない場合は編集せず報告する。既存のユーザー変更は保持する。
- [x] Step 2（FR1・NFR1・NFR2）: READMEの「AI 開発の進め方」の番号付き手順直後、「固定リリース・SHA-256、保存場所…」段落の前へ、下記2文と段落を区切る空行1行だけを追加する。既存行の変更・削除、別の位置への追加は行わない。
- [x] Step 3（FR1・FR3・NFR1・NFR2）: [検証手順](unit-test-instructions.md)の要件別5項目を確認し、`make check`を実行する。2文の完全一致・各1回・指定位置・既存本文の保持を確認する。重複、位置不整合、想定外の差分、チェック失敗は成功扱いにせず停止する。
- [x] Step 4（FR2・FR3）: このintent内の`code-summary.md`と`traceability.json`に、変更内容、要件への対応、実行コマンドと結果、未検証事項を記録する。完了した手順だけをチェックする。README差分と検証結果を提示して人の確認を待ち、公開・マージ・デプロイは行わない。

## 追記する全文

> 導入確認では、`/aidlc READMEへの小さな追記案を計画し、最初の承認ゲートで停止してください。実装・commit・push・PR作成・マージはしないでください。` のように、計画だけを依頼できます。
> 提示された承認対象ファイルと作業記録（intent）のパスを確認し、承認前に停止していることを確かめてください。

READMEでは引用記号を付けず、2行の本文とする。

## テスト方針

Testing Contractは`test-after`、`express`、`Minimal`。README本文の反映後、文書に適した最小の確認を実行する。アプリケーション、データモデル、API、画面、依存関係は追加しないため、これらの実装・テスト層は適用しない。

テストファイルとランナー設定の新設は非該当。既存のGit、POSIXコマンド、`make check`を使用し、検証コマンドと期待結果を`unit-test-instructions.md`に定義する。アプリ言語、テスト基盤、カバレッジ目標は新設しない。

## 制約と撤回

- Copilot Chat履歴の保持は対象外。Dev Container、Dockerfile、makefile、スクリプト、依存関係、承認保護、既存の実験記録は変更しない。
- ブランチ作成、commit、push、PR作成、承認代行、マージ、デプロイ、追加worktreeの作成は行わない。
- 文案・位置・受け入れ条件の変更が必要なら、承認済み要件を勝手に変更せず、再レビューと人の再承認を待つ。
- 撤回が必要な場合も、他の変更を戻さない。人の指示に基づいて今回追加した2文と空行だけを対象にする。
- 実フックの動作、Markdownの実表示、読者の理解向上は、この文書差分と構成チェックだけでは検証できない。

## Testing Contract

```json
{
  "version": 1,
  "methodology": "test-after",
  "source": "org",
  "ordering": "implement each applicable testable layer, then write and run that layer's tests.",
  "scope": "express",
  "test_strategy": "minimal",
  "project_type": "greenfield",
  "applicable_notes": [
    {
      "layer": "org",
      "text": "We treat tests as a first-class deliverable in every Bolt. The specific\nmethodology (TDD, BDD, ATDD, or classic test-after) is affirmed at\npractices-discovery and recorded in `team.md` under this heading with explicit\n`Methodology` and `Ordering` fields; Code Generation resolves those fields\nindependently from coverage, tooling, and scope notes.\n\nWhen no posture has been affirmed, our default per scope is:\n- **Methodology**: test-after\n- **Ordering**: implement each applicable testable layer, then write and run\n  that layer's tests.\n- `mvp`, `enterprise`, `feature`, `infra` add an 80% line-coverage\n  floor and CI execution before merge.\n- `bugfix`, `security-patch` add a targeted regression for the specific\n  bug/vulnerability and require the existing suite to remain green.\n- `express` uses the Minimal strategy: requirement-driven unit tests (one per\n  requirement, with a happy-path floor per component); existing tests remain\n  green.\n- `poc`, `refactor`, `workshop`, `classic` add no extra new-test floor and require the\n  existing suite to remain green.\n\nThe active `Test Strategy` still applies in every scope and determines test\nvolume/types. Scope floors are additive; they never reduce or replace the\nselected strategy.\n\nBuild and Test verifies defined coverage floors and affirmed quality targets;\nthey may not be weakened to make a step pass.\n\nAffirm a stricter posture in `team.md` if the team commits to one."
    },
    {
      "layer": "project",
      "text": "- Run `make check` and the focused checks for the change. Report exact commands, results, and unverified requirements.\n- `make check` covers infrastructure configuration and regression tests, not application behavior or real VS Code hook execution.\n- When application code is introduced, add its toolchain to the container, dependency lockfile where supported, and build, format, test and static-analysis commands to `make check`."
    }
  ],
  "obligations": {
    "strategy": "minimal",
    "strategy_volume": [
      "One verifiable test per requirement at the narrowest effective level.",
      "At least one happy-path unit test per component.",
      "Unit tests are the default; a bugfix/security scope floor may require an integration or E2E regression when that is the narrowest level that reproduces the defect."
    ],
    "scope_floor": [
      "Keep the existing test suite green.",
      "This scope adds no extra new-test floor beyond the selected test strategy."
    ],
    "combination_rule": "Apply every selected-strategy obligation and every scope-floor obligation; neither replaces the other, and a targeted scope regression may add the narrowest necessary test type beyond the strategy default."
  },
  "plan_profile": {
    "methodology": "test-after",
    "runner_step": "Bootstrap the minimal test runner/configuration and record the exact unit-scoped command.",
    "runner_ready_before_first_test": true,
    "testable_layers": [
      "Data model / database behavior",
      "Repository / data access",
      "Business logic",
      "API / endpoint",
      "Frontend behavior"
    ],
    "steps": [
      "Project structure and production configuration skeleton.",
      "Bootstrap the minimal test runner/configuration and record the exact unit-scoped command.",
      "Data model / database behavior - implement.",
      "Data model / database behavior - write and run its tests after implementation.",
      "Repository / data access - implement.",
      "Repository / data access - write and run its tests after implementation.",
      "Business logic - implement.",
      "Business logic - write and run its tests after implementation.",
      "API / endpoint - implement.",
      "API / endpoint - write and run its tests after implementation.",
      "Frontend behavior - implement.",
      "Frontend behavior - write and run its tests after implementation.",
      "Environment/build configuration.",
      "Documentation and traceability."
    ]
  },
  "input_sha256": "sha256:201919370cbe39f79f51639daa5002a01bfe8ce34a376aae6560a0a0a393f0bb",
  "contract_sha256": "sha256:faeb535134031441c7d3e78e5dad66bb567886c9e908f821ee79160cd0b662c9"
}
```
