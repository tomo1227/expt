# README追記のビルド・検証手順

## 対象と前提

- 対象は[承認済み実装計画](../code-generation/code-generation-plan.md)にあるREADMEの2文追記のみ。アプリケーション、コンパイル対象、Unit、外部サービスはない。
- Dev Containerを基準とし、リポジトリルートで既存のGit、grep、make、Python 3、POSIX shellを使う。依存追加、インストール、環境変数・設定変更は不要。
- [要件別検証手順](../code-generation/unit-test-instructions.md)のT1〜T5を使う。編集前専用のblob一致・未編集確認は[実装結果](../code-generation/code-summary.md)の過去の実行証拠であり、追記済みのREADMEに「未編集」を要求しない。
- 既存のユーザー変更は保持する。commit、push、PR作成・承認、マージ、デプロイ、ブランチ・worktree作成は実行しない。

## 共通検証

```sh
make check
```

期待値は終了コード0。実行内容はコンテナJSON、導入スクリプト構文、追跡済みAI-DLC構成、Git差分の空白検査。コンパイルや実際のVS Codeフックの検証ではない。個別チェックを重複して数えない。

## 文書の検証

```sh
grep -Fxc -- '導入確認では、`/aidlc READMEへの小さな追記案を計画し、最初の承認ゲートで停止してください。実装・commit・push・PR作成・マージはしないでください。` のように、計画だけを依頼できます。' README.md
grep -Fxc -- '提示された承認対象ファイルと作業記録（intent）のパスを確認し、承認前に停止していることを確かめてください。' README.md
git --no-pager diff --unified=3 -- README.md
git diff --numstat -- README.md
git diff --name-only
git diff --cached --exit-code -- README.md
git status --short
```

- 両grepの出力がそれぞれ厳密に`1`であること。0回・複数回はいずれも不合格。
- 差分が「AI 開発の進め方」の手順6直後、既存の「固定リリース・SHA-256、保存場所…」段落の前にある連続2文と空行だけであること。別位置・順序違いは不合格。
- 行数差分が`3 0 README.md`、追跡済み変更ファイルがREADMEのみ、ステージ済みREADME差分は終了0・出力なしであること。既存行の変更・削除、設定・依存の変更は不合格。
- intent内の未追跡記録は作業記録として区別し、削除やステージングをしない。

## 承認・記録・対応の確認

- T2: 発言原本と監査の回答・IDを照合する。今回有効な要件承認は`57c7c2a6`、計画承認は`9389273a`。実装完了承認は`779ee9af`。古い試行の承認や別の発言を流用しない。
- T3: コマンド・実測・未検証事項を[テスト結果](test-results.md)へ記録し、失敗や非該当を成功と数えない。
- T5: 日本語の承認済み全文との一致、および実表示・読者理解・実フック全体を未検証と明示していることを確認する。
- 次の必須の要件対応確認を1回実行し、[対応表](cross-unit-traceability.md)へ結果を記録する。

```sh
aidlc engine sensor-traceability --stage build-and-test
```

## 適用しない検証と異常時

- Minimal戦略のため、追加の統合・性能・セキュリティ検証手順は作成しない。アプリのビルド、単体テストランナー、行カバレッジ、E2E、負荷試験も非該当。実行した検証に数えない。
- CI Pipelineは今回の計画でSKIPのため、CI実行義務は`N/A`。CI成功やデプロイ準備完了を主張しない。
- チェック失敗・想定外の差分・承認不一致は具体的に記録して停止する。要件、閾値、承認済み計画を弱めず、保護を解除しない。
