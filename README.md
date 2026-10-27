# SoldFetch agent skills

Installable skills for public eBay listing research through [SoldFetch](https://soldfetch.com). Includes MCP-first guidance and a standard-library Python REST fallback.

## Install

```bash
npx skills add ricciflow-api/soldfetch-agent-skills
```

In Codex, ask the built-in installer to install `ebay-data` from this repository. You can also copy `skills/ebay-data` into your project's `.agents/skills/` directory.

## Configure

Connect [SoldFetch MCP](https://github.com/ricciflow-api/soldfetch-mcp) or export `SOLDFETCH_API_KEY` and run:

```bash
python3 skills/ebay-data/scripts/soldfetch_api.py search --keyword 'sony wh-1000xm5' --count 20
```

A successful search costs one request. The helper makes one request, validates key input limits, sends credentials only to SoldFetch, and rejects redirects. It does not install itself globally or alter your agent configuration.

## Validate

```bash
npm test
npm run test:live
```

[Documentation](https://docs.soldfetch.com) · [Examples](https://github.com/ricciflow-api/soldfetch-api-examples) · [MIT](LICENSE)
