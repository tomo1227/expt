# expt

AI と一緒に、小さな実験を実装・検証するリポジトリです。
アプリの言語は未選定です。まずは共通の開発環境と進め方を用意しています。

## 開発環境

前提は Docker と VS Code の Dev Containers 拡張です。

1. Docker を起動し、このリポジトリを VS Code で開く。
2. `Dev Containers: Reopen in Container` を実行する。
3. 初回作成時に `make check` が実行される。以後もコンテナ内で同じコマンドを使う。
4. Copilot を利用する場合は GitHub にサインインする。利用権限が必要です。

コンテナは Ubuntu 24.04 ベースで、Git、GitHub CLI (`gh`)、APM、make、Python 3 を利用できます。
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

1. `/issue-create` で AI に Issue を作成させる。
2. `/issue-review <Issue URL>` で仕様をレビューし、指摘を解消する。
3. 人が AI のレビューコメントを確認し、そのコメントに `+1` リアクションを付けて承認する。ハッシュの転記は不要。
4. `/implement <Issue URL> を実装して Draft PR を作成` と依頼する。
5. `/review <PR URL>` で AI がコードレビューする。修正後は再レビューする。
6. 人が CI とレビューを確認して、承認・マージを判断する。

詳細な承認条件、GitHub 認証、PR 作成条件は [AI 開発フロー](docs/ai-workflow.md)を参照してください。
承認前の実装を禁止し、Issue の仕様を変更した場合は再承認します。
現在は VS Code から工程ごとに呼び出す半自動構成であり、GitHub イベントによる自動起動は設定していません。
既存コンテナでは `Dev Containers: Rebuild Container` を実行すると `gh` が追加されます。

計画の補助には `/experiment-plan` を使えます。まとまった実験の結果は [テンプレート](docs/experiments/TEMPLATE.md)を基に `docs/experiments/YYYY-MM-DD-topic.md` へ記録してください。

プロンプトは [.github/prompts](.github/prompts) にあります。
スラッシュコマンドが表示されない場合は `Chat: Run Prompt...` から実行できます。
レビュー用プロンプトは読み取り中心の Ask モードを使いますが、独立した人手レビューや承認の代替ではありません。

## 検証と CI

```sh
make check
```

現在の検証対象は Dev Container 設定の JSON 構文と `git diff --check` のみです。
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