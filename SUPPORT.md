# Support

FEOS is maintained by volunteers, on a best-effort basis. There are no guaranteed response times or service levels.

| Need | Where |
|---|---|
| Question about using FEOS | Open an issue with a clear title and the `question` label |
| Bug report | Open an issue with steps to reproduce, the command, its output, and your versions |
| Feature or framework change | Open an issue to discuss it before sending a PR |
| Security vulnerability | Report it privately, as described in [SECURITY.md](SECURITY.md). Never use a public issue |
| Code-of-conduct incident | Report it privately, as described in [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) |

Before opening an issue, check [JUDGEMENT.md](JUDGEMENT.md) (known limitations) and existing issues.

## Compatibility

FEOS is tested in CI on Ubuntu with Python 3.12. It targets Claude Code (subagents, skills, hooks) and GitHub Copilot in VS Code (custom agents, instructions, prompt files).
Both tools change frequently, so check the adapter formats against their current documentation. Windows and macOS are used, but they are not part of CI.
