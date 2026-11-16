# Issue から PR までの AI 開発フロー

この構成は VS Code の Copilot から各工程を呼び出す半自動フローです。
Issue イベントやラベルで AI を自動起動する GitHub Actions は追加していません。
GitHub への書き込みは明示的に依頼された操作だけを行い、人の承認とマージを AI に代行させません。

## 工程

| 工程 | 担当・起動 | 完了条件 |
| --- | --- | --- |
| Issue 作成 | AI: `/issue-create <アイデア>` | 目的・対象外・成功条件・検証方法が記載された Issue |
| Issue レビュー | AI: `/issue-review <Issue URL>` | 指摘を解消し、現在の仕様ハッシュを添えた承認候補レビューをコメントに記録 |
| 承認 | 人のメンテナー | ハッシュ付きレビューコメントを確認し、そのコメントに `+1` リアクションを付ける |
| PR 実装 | AI: `/implement <Issue URL> を実装して Draft PR を作成` | 承認確認、実装、検証、Issue と承認情報を記載した Draft PR |
| PR レビュー | AI: `/review <PR URL>` | 最新差分を成功条件と照合し、指摘に対応 |
| マージ判断 | 人のメンテナー | CI とレビューを確認し、Draft を解除して承認・マージ |

Issue レビューは実装前の仕様レビューです。PR レビューは実装後のコードレビューです。
Issue の本文を修正したら、成功条件の変更に限らず再レビュー・再承認します。
PR の差分を修正したら最新の HEAD を再レビューします。古いレビューだけでマージしません。
実験の計画補助には `/experiment-plan` と [実験テンプレート](experiments/TEMPLATE.md)も使えます。

## GitHub 接続

コンテナに GitHub CLI (`gh`) を用意しています。GitHub 対応の MCP が利用可能なら、同等の操作をそちらで行っても構いません。
CLI を使う場合は、人がコンテナ内で認証を設定してください。

```sh
gh auth login
gh auth status
gh repo view --json nameWithOwner
```

トークンや認証コードを AI のチャットへ貼らないでください。認証情報をリポジトリやイメージに保存しないでください。
対象リポジトリと読み書き権限を確認し、認証できない場合は下書きを作成して停止します。

## 仕様ハッシュと承認

レビューする Issue のタイトルと本文だけを JSON として正規化し、SHA-256 を計算します。
Issue 番号とリポジトリはレビューコメントの URL とともに記録します。
次の例の `123` は対象 Issue 番号に置き換え、対象リポジトリ内で実行してください。

```sh
gh issue view 123 --json title,body | python3 -c 'import hashlib,json,sys; d=json.load(sys.stdin); s=json.dumps({"title":d["title"],"body":d["body"]},ensure_ascii=False,sort_keys=True,separators=(",",":")); print(hashlib.sha256(s.encode("utf-8")).hexdigest())'
```

AI の承認候補レビューを GitHub の Issue コメントに残します。Ask モードの出力は人が投稿するか、コメント投稿を別途 AI に明示的に依頼してください。

```text
Issue review: 承認候補
Specification: sha256:<計算したハッシュ>
指摘と対応確認: ...
検証計画: ...
```

人のメンテナーは内容を確認したうえで、AI の承認候補レビューコメントに GitHub の `+1`（親指を上げる）リアクションを付けます。
これが仕様への承認です。ハッシュや URL の転記、承認コメントの投稿は不要です。
リアクションが未表示の場合はコメントのリアクションメニューから選択します。専用ボタンの追加ではありません。
Issue 本文や別コメントへのリアクション、ラベル、従来の承認コメントだけではこの方式の承認になりません。
AI はレビュー投稿後にコメント URL と「このコメントに `+1` で承認」と案内し、承認リアクションを代行しません。

AI は実装前と PR 作成直前に以下をすべて確認します。

1. 対象 Issue の最新の仕様レビューが `Issue review: 承認候補` で、未解決の指摘がない。後続の要修正レビューを飛ばして古い承認候補を使わない。
2. そのコメントの `Specification: sha256:...` が現在のタイトル・本文のハッシュと一致する。
3. そのコメントのリアクション一覧に `content == "+1"` が存在し、投稿者が人（`user.type == "User"`）で、現在の権限が `write` / `maintain` / `admin` である。
4. リアクションの `created_at` がレビューコメントの `updated_at` より後である。同時刻を含め前なら、レビューを再確認した人にリアクションの削除・再追加を求める。
5. リアクションが現在も存在する。削除はその人の承認撤回とする。他の有効な承認があっても、明示的な撤回や反対意見があれば解消まで停止する。

レビューは編集せず、新しい仕様には新しいレビューコメントを投稿することを推奨します。
AI は PR にレビュー URL、承認者、リアクション ID・作成日時、仕様ハッシュを記録します。リアクション専用 URL の代わりにレビュー URL を使います。
CLI での取得例（`OWNER`、`REPO`、`COMMENT_ID`、`LOGIN` は取得した値へ置換）:

```sh
gh api repos/OWNER/REPO/issues/comments/COMMENT_ID
gh api --paginate repos/OWNER/REPO/issues/comments/COMMENT_ID/reactions
gh api repos/OWNER/REPO/collaborators/LOGIN/permission
```

取得は全ページを対象とし、権限や日時を確認できない場合は承認済みと推測せず停止します。Bot の反応は承認として扱いません。
レビュー後に矛盾する指摘や承認撤回があれば、解消されるまで停止します。
承認は仕様の承認であり、commit・push・PR 作成の実行許可とは別です。
リアクションを付けても AI 実装は自動起動しません。承認後に `/implement` を依頼してください。

## PR とレビュー

作業ブランチは `ai/issue-123-topic` のように Issue と対応させます。
ユーザーの作業中の差分を勝手に stash、削除、commit しません。
GitHub CLI で作成する場合は `gh pr create --draft` を使用し、[PR テンプレート](../.github/pull_request_template.md)の情報を含めます。
PR 作成が許可されていない場合はローカル実装と検証までで止めます。

PR レビューは最新の HEAD SHA、Issue の成功条件、変更差分、テスト結果、CI の状態を確認して行います。
レビュー結果には対象 HEAD SHA と根拠付きの指摘を記載します。投稿は別途依頼するか人が行います。
AI の「問題なし」は GitHub の人による Approve の代替ではありません。
仕様変更が必要なら Issue に戻り、再レビュー・再承認してから続けます。

## 制約

承認条件は現在、AI 向け指示と人の確認による運用ルールです。GitHub の権限制御として強制する仕組みではありません。
GitHub API では同じアカウントを操作する人と AI を区別できません。AI に人の認証で承認リアクションを代行させないことが運用上の前提です。
強制が必要なら GitHub 側で ruleset / branch protection を設定し、直接 push の禁止、必須 PR レビュー、必須 CI を適用してください。
これらのリモート設定変更や自動起動のための AI サービス認証は、この変更には含めていません。
CI の `make check` は現時点では開発基盤の設定チェックのみです。アプリ追加時に実際のテストを接続してください。