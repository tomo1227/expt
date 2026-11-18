"""Check the tracked Copilot distribution without installing or running hooks."""

import json
import re
import sys
from pathlib import Path


HOOKS = {
    "SessionStart": ("session-start", 1800),
    "UserPromptSubmit": ("record-human-turn", 1800),
    "PreToolUse": ("guard-tool-call", 1800),
    "PostToolUse": ("post-tool", 3600),
    "PreCompact": ("validate-state", 1800),
    "SubagentStart": ("subagent-start", 1800),
    "SubagentStop": ("log-subagent", 1800),
    "Stop": ("continue-workflow", 3600),
}


def check_project(root: Path) -> list[str]:
    errors = []
    version = (root / ".aidlc-version").read_text().strip()
    installer = (root / ".devcontainer/install-aidlc.sh").read_text()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        errors.append("Invalid .aidlc-version")
    if f"\nversion={version}\n" not in installer:
        errors.append("Installer version does not match .aidlc-version")
    if not re.search(r"\ninstaller_sha256=[0-9a-f]{64}\n", installer):
        errors.append("Installer SHA-256 must be pinned")

    hooks = json.loads((root / ".github/hooks/aidlc.json").read_text())
    if hooks.get("version") != 1 or set(hooks.get("hooks", {})) != set(HOOKS):
        errors.append("Copilot lifecycle hook registration is incomplete")
    for event, (target, timeout) in HOOKS.items():
        expected = [{
            "type": "command",
            "bash": f"aidlc engine adapter copilot {target}",
            "powershell": f"aidlc engine adapter copilot {target}",
            "timeoutSec": timeout,
        }]
        if hooks.get("hooks", {}).get(event) != expected:
            errors.append(f"{event}: official blocking hook command has changed")

    skills = sorted((root / ".github/skills").glob("aidlc*/SKILL.md"))
    if len(skills) != 43:
        errors.append("Expected 43 skills from the pinned Copilot distribution")
    for path in skills:
        text = path.read_text()
        header = text.split("---", 2)
        if len(header) != 3 or header[0] or (
            f"name: {path.parent.name}\n" not in header[1]
            or "description:" not in header[1]
        ):
            errors.append(f"{path.relative_to(root)}: invalid skill metadata")
    if not (root / ".github/skills/aidlc/SKILL.md").is_file():
        errors.append("Missing /aidlc entry point")

    agents = sorted((root / ".github/agents").glob("aidlc-*-agent.md"))
    if len(agents) != 14:
        errors.append("Expected 14 agents from the pinned Copilot distribution")
    for path in agents:
        if re.search(r"^model:", path.read_text(), re.MULTILINE):
            errors.append(f"{path.relative_to(root)}: do not pin the user's model")

    instructions = (root / "AGENTS.md").read_text()
    if instructions.count("<!-- BEGIN AI-DLC:agents -->") != 1:
        errors.append("Missing or duplicated managed AI-DLC onboarding")
    if instructions.count("<!-- END AI-DLC:agents -->") != 1:
        errors.append("Missing managed AI-DLC onboarding terminator")
    for name in ("org", "team", "project"):
        if f"@aidlc/active-memory/{name}.md" not in instructions:
            errors.append(f"Missing managed memory import: {name}")
        if not (root / f"aidlc/spaces/default/memory/{name}.md").is_file():
            errors.append(f"Missing shared memory: {name}")
    policy = (root / "aidlc/spaces/default/memory/project.md").read_text()
    if "\nMode: strict\n" not in policy:
        errors.append("Project guard policy must remain strict")
    for obsolete in ("issue-create", "issue-review", "implement"):
        if (root / f".github/prompts/{obsolete}.prompt.md").exists():
            errors.append(f"Retired workflow prompt is present: {obsolete}")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    try:
        errors = check_project(root)
    except (OSError, ValueError) as error:
        print(f"AI-DLC configuration check failed: {error}", file=sys.stderr)
        return 1
    for error in errors:
        print(f"AI-DLC configuration check failed: {error}", file=sys.stderr)
    if errors:
        return 1
    print("AI-DLC tracked configuration OK (interactive hooks not verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
