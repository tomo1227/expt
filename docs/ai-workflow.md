# AI-DLC 開発フロー

VS Code / GitHub Copilotで、公式AI-DLC `2.11.4` を使用します。
Issueイベントによる自動起動ではなく、人が `/aidlc` から開始します。
AI-DLCの承認ゲートとGitHubへの公開許可は別です。人の承認・PR承認・マージをAIに代行させません。

## 導入・復元

基準はDev Containerです。既存環境は `Dev Containers: Rebuild Container` で再構築してください。
Dockerfileはコンテナユーザーとして固定版CLIを導入し、フックからも使えるようPATHを設定します。
コンテナ作成時は `make aidlc-setup && make check` を実行します。

```sh
# コンテナを再構築せず既存のLinuxコンテナに導入する場合
sh .devcontainer/install-aidlc.sh

# clone後・実行用生成物を失った場合
make aidlc-setup
aidlc --version
aidlc doctor
make check
```

`.aidlc-version` がプロジェクトの固定バージョンです。`aidlc config --harness copilot --yes` はこのpinを使います。
未導入のpinを指定した場合は勝手に最新版へ切り替えず、先に同じ固定版を導入してください。
シェルで `aidlc` が見つからなければ、インストーラーが表示するPATH設定を適用します。起動済みのVS CodeへCLIを追加した場合は、VS Codeを完全に終了して開き直す必要があります。

### 配布元と整合性

- リリース: [v2.11.4](https://github.com/awslabs/aidlc-workflows/releases/tag/v2.11.4)
- ソース: [`61fdb122428d86b56b7e8d598787095f2c97d3e1`](https://github.com/awslabs/aidlc-workflows/tree/61fdb122428d86b56b7e8d598787095f2c97d3e1)
- インストーラーSHA-256: `3ccd128b79c9cc7607fa811c4c6d1dedd888e516af29d942b5b8679f48ebdb83`
- 導入スクリプトはバージョン付きURLと固定SHA-256を使います。公式インストーラーがさらに配布物のチェックサムとリリースメタデータを確認します。対応する `gh` がある場合はprovenanceも検証しますが、この環境の古い `gh` ではprovenance検証を利用できません。チェックサム検証は実施されます。
- native版なのでBun / Node.jsや上流開発用の依存は不要です。モデル・プロバイダーは変更しません。

公式生成物の出典・ライセンスは [third_party/aidlc](../third_party/aidlc) を参照してください。

### VS Code側の前提

公式の[固定版Copilotガイド](https://github.com/awslabs/aidlc-workflows/blob/61fdb122428d86b56b7e8d598787095f2c97d3e1/docs/guide/harnesses/copilot.md)に従います。

1. VS Code 1.130以上とGitHub Copilotを用意する。CLI版Copilotは必須ではありません。
2. コマンドパレットから `Workspace: Manage Workspace Trust` を開き、内容を確認して信頼できるWorkspaceで作業する。
3. 設定で `chat.useHooks` を有効にする。組織ポリシーで禁止されている場合は停止し、制限を報告する。
4. 新しいチャットを開いて `/aidlc --doctor` を実行する。Agent Debug Logsで実フックの実行も確認する。

`aidlc doctor` はVS CodeのTrust・設定・組織ポリシーをすべて検証できません。
「AIDLC hooks have not run」警告を無視して承認保護が働いたと判断しないでください。
HooksはPreview機能です。必要機能が使えない場合、承認保護を無効化する回避策を採らず停止します。

## 工程

| 工程 | 担当・起動 | 完了条件 |
| --- | --- | --- |
| 開始 | 人: `/aidlc <要求またはIssue URLと依頼>` | 要求を整理し、作業記録と適した計画を提示 |
| 計画 | AIと人 | 対象・対象外・成功条件・検証方法・工程を確認 |
| 承認ゲート | 人 | AI-DLCが提示する対象成果物・版を確認して回答 |
| 実装・検証 | AI | 承認済みの範囲で最小の変更を行い、対象の検証を実行 |
| Draft PR | 人の明示依頼を受けたAI | 承認記録・検証結果・関連Issueを添えて公開 |
| PR レビュー | AI: `/review <PR URL>` | 最新HEADを成功条件と照合。工程内レビューとは別の助言 |
| マージ判断 | 人のメンテナー | CIとレビューを確認して、Draftを解除して承認・マージ |

例:

```text
/aidlc https://github.com/tomo1227/expt/issues/123 の要求を整理して計画を作って
/aidlc compose 小さな実験の計画を提案して
```

提示された計画や成果物を読んでから、承認ゲートの質問に回答します。
AIは実際の人の回答を公式の処理に渡し、作業記録・監査記録へ残します。AIのレビュー推薦やIssueの記述を人の回答とみなしません。
承認対象のパス・版と回答記録を対応付け、確認できない場合は停止します。
要求・成功条件・承認済み成果物が変わったら、その変更を再レビューし、人の承認を得てから続けます。
Guard Policyはプロジェクトメモリで `strict` に固定し、承認を省略するために弱めません。

GitHubへの公開を行う場合は、別途たとえば「この承認済みの範囲を実装し、作業ブランチを作成してcommit・pushし、Draft PRを作成して」と依頼してください。
工程の承認だけではこれらの操作を許可したことにはなりません。

### 中断・再開

同じWorkspaceの新しいチャットで `/aidlc` を実行すると、現在の作業記録を確認して最後のチェックポイントから再開します。
別cloneではローカルcursorが共有されないため、`/aidlc intent list` で記録を確認し、`/aidlc intent <name>` で対象を選びます。
版の古い成果物や別intentの承認を使わないでください。
実験の補助に `/experiment-plan` と[実験テンプレート](experiments/TEMPLATE.md)も使えますが、計画補助だけでは承認ゲートを通過しません。

### 保存場所とGit追跡

| 場所 | 扱い |
| --- | --- |
| `.aidlc-version` | 追跡する。固定リリース |
| `.github/skills/aidlc*/`、`.github/agents/aidlc-*-agent.md`、`.github/hooks/aidlc.json` | 公式生成物を追跡する。直接改変せず固定版から復元 |
| `AGENTS.md` のAI-DLC管理ブロック | 追跡する。公式importを維持 |
| `.aidlc/` | 追跡しない実行用生成物。`make aidlc-setup` で復元 |
| `aidlc/spaces/<space>/memory/` | 追跡する。プロジェクト固有ルールは `project.md` |
| `aidlc/spaces/<space>/intents/<record>/` | 状態・成果物・分割監査ログをレビューして追跡する |
| `aidlc/active-space`、active-intent、active-memory、セッション等 | 公式gitignoreに従うローカル状態 |
| `.vscode/` | ローカル設定として追跡しない。Trust・Hooksの実行可否は人が確認 |

共有記録にも秘密情報を書かないでください。`git add aidlc/` を機械的に実行せず、今回の変更に必要な記録だけを確認して公開します。
APM管理物は維持します。現行のAPMロックファイルに旧フローのプロンプトは含まれず、APMとAI-DLCの管理対象も分離しています。
依存更新や `apm install` 後は差分を確認し、旧指示や管理対象の衝突が追加されていないか確認してください。

## 旧フローからの移行

| 旧導線 | 新導線 |
| --- | --- |
| `/issue-create` | IssueはGitHubで作成するかAIに作成を明示依頼し、作業は `/aidlc <要求またはIssue URL>` |
| `/issue-review` | `/aidlc` 内で要求・計画・成果物をレビュー |
| ハッシュ付きレビューへの `+1` | AI-DLCが提示する対象成果物を確認し、承認ゲートに人が回答 |
| `/implement` | `/aidlc` の承認済み工程から進む。公開操作は別途明示依頼 |
| `/review` | 維持。最新PRまたは未commit差分への助言。旧ハッシュ承認は要求しない |
| `/experiment-plan` | 維持。AI-DLCで計画を作る場合は `/aidlc compose <要求>` |

`/issue-create`、`/issue-review`、`/implement` のプロンプトは撤去しています。
過去の実験記録は履歴として保持します。この移行のIssue #2とPRだけは旧フローの仕様承認を引き継ぎ、PR作成直前にも確認します。
移行後の新規タスクに旧方式を並行して要求しません。

## GitHub 接続

GitHub CLI (`gh`) の認証は人が設定してください。認証情報をチャット・リポジトリ・イメージへ保存しません。

```sh
gh auth login
gh auth status
gh repo view --json nameWithOwner
```

対象リポジトリと読み書き権限を確認し、認証できない場合は公開せず停止します。

## PR とレビュー

作業ブランチは `ai/issue-123-topic` のようにIssueと対応させます。
ユーザーの作業中の差分を勝手にstash・削除・commitしません。
公開を依頼された場合だけ `gh pr create --draft` を使い、[PRテンプレート](../.github/pull_request_template.md)に沿って記載します。
AI-DLC作業記録、承認対象の成果物と版、人の回答記録、関連Issue、検証結果・未検証事項を記載します。
公開直前にも承認対象が変わっていないことと、撤回・未解決指摘がないことを確認します。

PRレビューは最新HEAD SHA・承認済み成功条件・差分・テスト・CIを照合し、対象HEADと根拠付きの指摘を残します。
コメント投稿は明示依頼がある場合だけ行います。AIの「問題なし」は人のApproveの代替ではありません。
仕様変更が必要なら対象成果物を更新し、再レビュー・再承認してから続けます。
Constructionのworktree / Unit / Boltのmerge・land操作も自動マージ禁止の対象です。

## 更新・撤去・復旧

更新は実験として扱います。リリース・ソースcommit・インストーラーSHA-256を確認し、`.aidlc-version` と導入スクリプトの固定値を同時に更新します。
対象版を導入して `make aidlc-setup` を実行し、生成物の差分・ライセンス・APMとの競合を確認して、`make check` と対話検証を再実施します。
スキル・エージェント数が変わる場合は構成チェックも更新します。`aidlc update` は通常の復元手順には使いません。

撤去時は人の明示依頼のもと、追跡済みAI-DLC生成物と管理ブロックを特定して削除します。
作業記録 `aidlc/` は監査・復帰に必要なので、バックアップして保持します。APM管理物や無関係な設定は削除しません。
ローカルのVS Code設定は人が確認し、必要なAI-DLC由来の変更だけを戻します。
共有コンテナ等で他プロジェクトがCLIを使う場合はアンインストールしません。不要と確認できたユーザーだけ `aidlc uninstall` を実施します。
復旧は直前に動作確認したGitリビジョンを新しい作業ブランチで復元し、その版のCLIを再導入して `make aidlc-setup` を実行します。
削除や復元は対象を特定して行い、未commitのユーザー変更や共有記録を強制的に破棄しません。

## 検証と制約

CIの `make check` はJSON・シェル構文・追跡済みAI-DLC構成・空白の検証です。
VS Codeの実フック、承認待ち、再開は手動で別途検証し、実験記録に残してください。アプリ追加時に実際のテストを接続します。

フックによるゲート保護と人の確認は、GitHubの権限制御そのものではありません。人の認証を使ってAIに承認回答やPR承認を代行させないことが前提です。
強制が必要なら、人がruleset / branch protectionを設定し、直接push禁止・必須PRレビュー・必須CIを適用します。
これらのリモート設定変更や、自動起動のためのAIサービス認証は導入範囲に含めていません。
