# MKT Skills

129 marketing skills for AI agents: a diagnosis router (`00-router`) plus 128 skills across 20 sections covering market research, customer research, positioning, offers, copywriting, creative strategy, paid ads, SEO, funnels, CRO, sales, retention, referrals, measurement, experimentation, growth, and operations.

Works with Claude Code, OpenAI Codex, Cursor, Windsurf, GitHub Copilot, and any agent that supports the [Agent Skills spec](https://agentskills.io).

Built by [Vince Servidad](https://www.vinceservidad.com/) · Website: <https://mktskills.com>

## Install

### Option 1: CLI Install (all AI agents)

```bash
# Install all 129 skills
npx skills add vinceservidad/mkt-skills

# List all available skills
npx skills add vinceservidad/mkt-skills --list

# Install specific skills
npx skills add vinceservidad/mkt-skills --skill 00-router 07-offer-design 11-paid-search
```

### Option 2: Claude Code Plugin

Install everything or pick only the sections you need:

```bash
# All 129 skills
/plugin install mkt-skills --marketplace vinceservidad/mkt-skills

# Or install modular packs (start with the router, then add the sections you need)
/plugin install mkt-core --marketplace vinceservidad/mkt-skills
/plugin install mkt-q1-audience --marketplace vinceservidad/mkt-skills
/plugin install mkt-q2-offer --marketplace vinceservidad/mkt-skills
/plugin install mkt-q3-message --marketplace vinceservidad/mkt-skills
/plugin install mkt-q4-reach --marketplace vinceservidad/mkt-skills
/plugin install mkt-q5-decide --marketplace vinceservidad/mkt-skills
/plugin install mkt-q6-after --marketplace vinceservidad/mkt-skills
/plugin install mkt-q7-improve --marketplace vinceservidad/mkt-skills
/plugin install mkt-q8-run --marketplace vinceservidad/mkt-skills
```

### Option 3: OpenAI Codex Plugin

```bash
codex plugin marketplace add vinceservidad/mkt-skills
```

Then run `/plugins` inside Codex and select **mkt-skills**.

### Option 4: ChatGPT and Claude.ai (no login required)

Add the read-only remote MCP connector:

```text
https://mktskills.com/mcp/open
```

Setup help: <https://mktskills.com/support>

## About this repository

This repository is generated from the MKT Skills source and updated on each release. Please open issues here; pull requests that edit `skills/` directly will be overwritten on the next sync.

## License

MIT. See [LICENSE](https://github.com/vinceservidad/mkt-skills/blob/main/LICENSE).
