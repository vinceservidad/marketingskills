# MKT Skills

31 marketing skills for AI agents: Google Ads, Meta Ads, SEO, CRO, copywriting, tracking, pricing, retention, growth strategy and more. Each skill is a folder with a `SKILL.md`, its references, and the shared operating rules it links to (`_shared/`).

The skills put business outcomes first. They label facts, calculations and guesses separately, never invent benchmarks or results, and don't change live campaigns, budgets or tracking without approval.

## Install

```bash
npx skills add vinceservidad/mkt-skills
```

The command finds the agents on your machine (Claude Code, Codex, Cursor, GitHub Copilot, Gemini CLI, Windsurf, OpenCode and others) and installs the skills where each one looks for them.

List the skills first, or install one:

```bash
npx skills add vinceservidad/mkt-skills --list
npx skills add vinceservidad/mkt-skills --skill google-ads
```

Other ways to use them:

- **Claude Code plugin (skills + connector):** `/plugin marketplace add https://mktskills.com/marketplace.json`, then `/plugin install mkt-skills@mkt-skills`
- **Connector for ChatGPT and Claude, no login:** `https://mktskills.com/mcp/open`
- **Zip downloads:** <https://mktskills.com/downloads/mkt-skills-skills.zip>

Setup help: <https://mktskills.com/support>

## About this repository

This repository is generated from the MKT Skills source and updated on each release. Please open issues here; pull requests that edit `skills/` directly will be overwritten on the next sync.

## License

MIT. See [LICENSE](https://github.com/vinceservidad/mkt-skills/blob/main/LICENSE).
