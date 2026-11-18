# README追記のビルド・テスト概要

## 検証範囲と目標の出典

[実装計画](../code-generation/code-generation-plan.md)のTesting Contractは`test-after`・`express`・`Minimal`。[検証手順](../code-generation/unit-test-instructions.md)のT1〜T5を、この文書変更に適用する目標として全件採用した。NFR RequirementsとNFR Designの成果物は存在せず、アプリの追加目標はない。要件はFR1〜FR3・NFR1〜NFR2、今回の反映完了条件はAC6〜AC8。

生成した追加テスト指示ファイルはない。[ビルド・検証手順](build-instructions.md)と既存のT1〜T5を使い、新しいランナー・依存・設定・テストファイルを導入しない。

## Target Verification Matrix

| Target ID | Source | Expected | Actual | Evidence | Owning Stage | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| DOC-T1 | unit-test-instructions.md / T1、FR1・AC6 | 承認済み全文が各1回、指定位置・順序 | 両grep出力1、手順6直後の1ハンク | [テスト結果](test-results.md) / T1 | build-and-test | Met |
| DOC-T2 | unit-test-instructions.md / T2、FR2・AC8 | 実際の要件・計画承認後の編集、公開せず確認待ち | 実発言の承認3件を照合、公開操作なし、本工程の人の確認待ち | [テスト結果](test-results.md) / T2 | build-and-test | Met |
| DOC-T3 | unit-test-instructions.md / T3、FR3・AC7 | make check終了0、正確な検証結果の記録 | make check終了0、T1〜T5と検証限界を記録 | [テスト結果](test-results.md) / T3 | build-and-test | Met |
| DOC-T4 | unit-test-instructions.md / T4、NFR1・AC6 | 追加3行・削除0行、追跡済み変更はREADMEのみ | 3行追加・0行削除、READMEのみ、ステージ済み差分なし | [テスト結果](test-results.md) / T4 | build-and-test | Met |
| DOC-T5 | unit-test-instructions.md / T5、NFR2・AC7 | 承認済み日本語文案と一致し、検証限界を明記 | 日本語全文一致、実表示・読者理解・実フック全体は未検証と明記 | [テスト結果](test-results.md) / T5 | build-and-test | Met |
| CI-EXECUTION | Testing Contract / obligations、実行計画ci-pipeline | 今回の計画での適用有無 | CI PipelineはSKIP | aidlc-state.md / Stage Progress | ci-pipeline | N/A |

CI行の理由は「the plan runs no CI Pipeline」。文書変更に適用される5目標の代わりに`N/A`を使わない。アプリの行カバレッジ目標は本変更に存在せず、80%などの新しい閾値を追加・緩和しない。

## 最終判定

- 文書検証は5項目中5項目成功、失敗0、スキップ0。上記の適用目標5件はすべて`Met`で、未確定の適用目標はない。CIの`N/A`行をテスト成功数に含めない。
- `make check`は終了0。アプリのコンパイルではなく、既存の構成・回帰・空白チェックが成功した。
- [最終対応表](cross-unit-traceability.md)は全5要件に対応があり、必須の要件対応確認の出力は`pass: true`、`uncovered: []`だった。これは行カバレッジの100%を意味しない。
- 文書変更として検証済み。結果は人の承認待ちであり、本工程の承認を代行しない。デプロイ準備完了とは判定しない。
- README・承認済み計画・検証手順は本工程では変更せず、本工程の4記録だけを作成した。追加の統合・性能・セキュリティ検証手順はMinimal戦略により非該当。

## 検証限界

Markdownの実表示、読者の理解向上、実際のVS Codeフック全体・承認後再開は未検証。これらを必須の文書検査の成功で代用しない。アプリのビルド・テスト、統合・性能・脆弱性スキャンは非該当で、実行済みとは扱わない。公開やデプロイの準備完了・許可も含まない。
