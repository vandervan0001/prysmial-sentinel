# Codex and Claude Code

Both clients use the same nine `SKILL.md` entry points, reference files and Python tools. The skill instructions identify absolute library and target paths before running commands. Client permissions and available tools still determine which checks can run.

| Client | Distribution | Audit command |
|---|---|---|
| Codex | `python3 scripts/install.py --apply` from the clone | `$cyber-audit` |
| Claude Code | Plugin marketplace or local plugin directory | `/prysmial-sentinel:cyber-audit` |

## Codex

Run `python3 scripts/install.py` to preview the links, then add `--apply`. The installer uses `$CODEX_HOME/skills`, or `~/.codex/skills` when unset. An explicit `--dest` selects another skills directory. Existing conflicting files are never overwritten. Keep the source clone in place.

## Claude Code

In Claude Code, add the repository and install the plugin:

```text
/plugin marketplace add vandervan0001/prysmial-sentinel
/plugin install prysmial-sentinel@prysmial-sentinel
```

Follow the client's installation summary to reload plugins or start a new session. In the project to review:

```text
/prysmial-sentinel:cyber-audit Review this project. Start with local files and tests. Report confirmed findings, evidence and untested areas.
```

For a local checkout, start Claude Code from the target project with:

```bash
claude --plugin-dir /absolute/path/prysmial-sentinel
```

The plugin packages the whole library so links between domains, scripts and examples stay inside its directory. Domain commands use the same namespace, for example `/prysmial-sentinel:cyber-ot`. Codex UI metadata in `agents/openai.yaml` belongs to Codex; Claude discovers the shared skills through its plugin layout.

To update an installed copy, refresh the marketplace and update the plugin. Repository maintainers must keep the plugin version aligned with `VERSION` when releasing.

The integration uses Claude Code's documented [skill format](https://code.claude.com/docs/en/skills), [plugin layout](https://code.claude.com/docs/en/plugins-reference) and [marketplace installation](https://code.claude.com/docs/en/plugin-marketplaces). It targets Claude Code. Uploading this multi-skill repository to Claude's web interface is not a supported installation route.
