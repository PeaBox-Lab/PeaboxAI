# PeaBox AI Workbench Roadmap

This roadmap reflects the direction of PeaBox AI Workbench after v4.1. It is
organized around small, shippable releases rather than large, indefinite
milestones. Versions may shift as maintainers and contributors land work; the
issue tracker is the source of truth for what is in progress.

## Guiding principles

- **Local-first and private by default** — cloud providers are opt-in.
- **Your models, your APIs** — no vendor lock-in; OpenAI-compatible endpoints stay first-class.
- **Boring, inspectable technology** — SQLite, Streamlit, standard Python.
- **Ship small, keep it stable** — every release must install cleanly and pass CI on Windows and Linux.

## v4.1 — Stabilization (current)

- Real pytest suite (storage, attachments, provider adapters with mocks, headless UI smoke tests)
- Working CI (compile check + tests on Windows/Linux, Python 3.11–3.13)
- Bug fixes: Anthropic system prompts, Ollama `num_predict`, export crash, SQL LIKE escaping
- Delete confirmation now enforced; `PEABOX_DATA_DIR` relocation support

## v4.2 — Chat experience

- Streaming responses (Server-Sent Events) with a Stop button
- Regenerate / edit-and-resend messages
- Copy buttons, token/cost display per message, conversation token counters
- Keyboard shortcuts and a compact density option
- Model response comparison (two models, same prompt, side by side)

## v4.3 — Knowledge and RAG

- Per-project workspaces with isolated history and configuration
- Local document index (embedded chunks in SQLite via `sqlite-vec` or Chroma)
- Retrieval-augmented generation with inline source citations
- Prompt library with variables and sharing (export/import)
- Conversation search across content, not just titles

## v4.4 — Agents and tool use

- Tool / function calling for tool-capable models
- MCP (Model Context Protocol) client support
- Human-in-the-loop approval for tool execution
- Provider fallback and smart routing (fast model for easy prompts, strong model for hard ones)
- Optional, sandboxed local code execution for analysis tasks

## v4.5 — Observability and cost

- Usage and cost analytics dashboard (per model, per conversation, per day)
- Budget caps and alerts for paid providers
- Local benchmarking harness (latency, tokens/sec, quality rubrics)
- Backup and restore (export/import the whole `PEABOX_DATA_DIR`)

## v5.0 — Teams and enterprise

- Authentication (local accounts, optional OIDC/SSO)
- Role-based access control and shared workspaces
- Centralized secret management (Vault, 1Password, Azure Key Vault)
- Audit logs and conversation retention policies
- Open WebUI-compatible and LiteLLM gateway integration guides

## Future exploration

- Extension / plugin system with a marketplace
- Desktop packaging (pywebview or Tauri shell) and signed installers
- Mobile companion via PWA
- Offline-first mode with fully local embeddings and models
- i18n and accessibility audit (WCAG 2.1 AA)
