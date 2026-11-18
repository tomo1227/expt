# AI-DLC distribution

- Upstream: https://github.com/awslabs/aidlc-workflows
- Release: `v2.11.4`
- Source commit: `61fdb122428d86b56b7e8d598787095f2c97d3e1`
- License: [MIT No Attribution (MIT-0)](LICENSE).

The official native CLI generates the Copilot skills, agents, hooks and managed
`AGENTS.md` / `.gitignore` blocks tracked in this repository. Shared memory files
are seeded from that release; `aidlc/spaces/default/memory/project.md` contains
this repository's additional policy. The ignored `.aidlc/` engine is restored
by `make aidlc-setup`, not vendored here.

See [the workflow](../../docs/ai-workflow.md) for verified downloads, setup,
updates and removal.
