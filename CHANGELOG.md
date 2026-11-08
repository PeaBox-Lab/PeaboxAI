# Changelog

## 4.1.0
- Fixed Anthropic requests silently dropping the configured system prompt (now sent as the top-level `system` parameter).
- Fixed Ollama `Max output tokens` being ignored (mapped to `num_predict`).
- Fixed `export_conversation()` crashing with `TypeError` on missing conversations (now raises a clear `ValueError`).
- Fixed conversation search treating `%` and `_` as SQL wildcards.
- Fixed a `KeyError` crash when a provider's Base URL was not configured; a clear error is shown instead.
- Settings "Confirm destructive actions" is now enforced before deleting a conversation.
- Settings page shows whether an API key is saved; API keys can no longer crash keyring-backed systems without a credential store.
- Direct Ollama is preferred as the default provider on fresh installs.
- Added `PEABOX_DATA_DIR` environment variable to relocate the data directory (useful for portable installs and tests).
- Removed unused `pandas` dependency.
- Replaced the placeholder test checklist with a real pytest suite (storage, attachments, providers with mocks, headless UI smoke tests) and a working CI workflow.

## 4.0.0
- Settings and credentials removed from main chat interface.
- Added provider management, defaults, search, pinning, archiving, renaming and export.
- Preserved v3 database/config paths and added automatic schema migration.
