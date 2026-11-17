# expt

AI と一緒に、小さな実験を実装・検証するリポジトリです。
アプリの言語は未選定です。まずは共通の開発環境と進め方を用意しています。

## 開発環境

前提は Docker と VS Code の Dev Containers 拡張です。

1. Docker を起動し、このリポジトリを VS Code で開く。
2. `Dev Containers: Reopen in Container` を実行する。
3. 初回作成時に `make aidlc-setup && make check` が実行される。以後の検証もコンテナ内で `make check` を使う。
4. Copilot を利用する場合は GitHub にサインインする。利用権限が必要です。

コンテナは Ubuntu 24.04 ベースで、Git、GitHub CLI (`gh`)、APM、AI-DLC、make、Python 3 を利用できます。
Python は設定検証用で、アプリの言語を指定するものではありません。
ソースはホストからマウントされるため、コンテナ内の変更はホストにも反映されます。
Docker ソケットの共有、特権モード、AI 操作の無条件承認は設定していません。

Dev Containers CLI を利用する場合:

```sh
devcontainer up --workspace-folder .
devcontainer exec --workspace-folder . make check
```

### Agent Package Manager

[APM](https://github.com/microsoft/apm) CLI を公式の Linux / macOS 向けインストーラーで導入しています。
バージョンは Dockerfile の `APM_VERSION` で `0.35.1` に固定しています。
インストーラー自体は公式 URL の最新版を取得するため、完全な再現性を保証するものではありません。
既存コンテナでは `Dev Containers: Rebuild Container` を実行してから確認してください。

```sh
apm --version
apm --help
```

このリポジトリは `microsoft/apm-sample-package#v1.0.0` を Copilot 向けに導入しています。
`apm.yml` が依存関係、`apm.lock.yaml` が解決したコミットと展開ファイルのハッシュを記録します。
展開された指示・エージェント・プロンプト・スキルもレビュー可能なソースとしてバージョン管理し、`apm_modules/` はコミットしません。

```sh
# clone 後、リポジトリのルートで依存関係を復元
apm install

# 依存関係と展開ファイルを検査
apm audit --ci
```

パッケージの内容と推移依存も追加前に確認してください。サンプルの推移依存は上流で参照が未固定ですが、ロックファイルには解決済みコミットが記録されます。依存を更新するときは差分をレビューしてください。

## AI 開発の進め方

共通ルールは [AGENTS.md](AGENTS.md) にまとめています。
VS Code / Copilot がルートの指示ファイルを読み込む構成です。
別の AI ツールでは、対応状況を確認し、必要ならこのファイルを明示的にコンテキストへ追加してください。

公式 [AI-DLC](https://github.com/awslabs/aidlc-workflows) `2.11.4` のCopilot構成を使用します。
既存コンテナは `Dev Containers: Rebuild Container` でCLIを追加し、VS Codeを開き直してください。

```sh
make aidlc-setup
aidlc --version
aidlc doctor
```

1. VS Code 1.130以上で、信頼済みWorkspaceと `chat.useHooks` 有効を確認する。組織ポリシーでHooksが禁止されていれば停止する。
2. 新しいCopilotチャットで `/aidlc --doctor` を実行し、実フックの動作を確認する。
3. `/aidlc <作りたいもの、またはIssue URLと依頼内容>` から開始する。
4. AIが提示する計画・成果物を確認し、人が各承認ゲートへ回答する。変更時は再レビュー・再承認する。
5. 公開する場合は、ブランチ作成・commit・push・Draft PR作成を明示的に依頼する。承認だけでは公開しない。
6. `/review <PR URL>` で最新差分への助言を受け、人がCI・レビューを確認して承認・マージを判断する。

固定リリース・SHA-256、保存場所、開始・中断・再開、更新・撤去、旧コマンドからの移行は [AI開発フロー](docs/ai-workflow.md)を参照してください。
旧 `/issue-create`、`/issue-review`、`/implement` と独自ハッシュ承認は新規タスクでは使用しません。
GitHubイベントでAIを自動起動する設定はありません。人の承認・PR承認・マージはAIに代行させません。

計画の補助には `/experiment-plan` を使えます。まとまった実験の結果は [テンプレート](docs/experiments/TEMPLATE.md)を基に `docs/experiments/YYYY-MM-DD-topic.md` へ記録してください。

プロンプトは [.github/prompts](.github/prompts) にあります。
AI-DLCのスキルは [.github/skills](.github/skills) にあり、`make aidlc-setup` で公式配布物から復元できます。
補助プロンプトが表示されない場合は `Chat: Run Prompt...`、AI-DLCが表示されない場合はバージョン・スキル検出・Trustを確認して新しいチャットを開始してください。
レビュー用プロンプトは読み取り中心の Ask モードを使いますが、独立した人手レビューや承認の代替ではありません。

## 検証と CI

```sh
make check
```

現在の検証対象はDev Container設定のJSON構文、導入スクリプトのシェル構文、追跡済みAI-DLC構成（pin・フック・スキル・承認保護）、`git diff --check` です。
CLI診断や構成チェックだけで、VS Codeの実フック実行・承認前停止・承認後再開を検証したことにはしません。[実験記録](docs/experiments/2026-11-17-aidlc-v2.md)に手動確認の結果を記録します。
アプリのテスト、ビルド、フォーマット、静的解析はまだありません。
CI は Ubuntu ランナー上で `make check` を直接実行します。Dev Container のビルド・起動確認は行いません。
ベースイメージはタグ指定のため、完全な再現性が必要になったら digest 固定を検討してください。

最初のアプリを追加するときは、以下を同じ変更に含めます。

- コンテナへの言語ツールチェーン追加とバージョン指定。
- 依存定義と、対応していればロックファイル。
- Makefile へのテスト・ビルド・フォーマット検証・静的解析の追加と `make check` への接続。
- 回帰テスト、起動コマンド、必要なポートや環境変数の文書化。

秘密情報はローカルの `.env` 等に置き、AI への入力や実験記録に含めないでください。
共有する `.env.example` にはダミー値だけを記載します。