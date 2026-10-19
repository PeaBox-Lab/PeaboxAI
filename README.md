A local-first, multi-provider LLM workbench for chatting with local, remote and cloud AI models. 
Built with Streamlit for Ollama, OpenAI, Anthropic, Gemini, Groq, OpenRouter, LiteLLM and OpenAI-compatible AI models.


# PeaBox Streamlit LLM Workbench v4

A direct upgrade of v3, preserving SSH Ollama, Direct Ollama, OpenAI-compatible providers, Anthropic, file extraction, vision inputs, model discovery, reasoning controls and local SQLite history.

## v4 upgrades
- Dedicated **Settings & API Vault** page
- Provider enable/disable, preferred model, connection testing and model discovery
- Additional LM Studio, Mistral and Together AI presets
- Search, pin, archive, rename and JSON export conversations
- Workbench-level default provider and system prompt
- Cleaner Chat, Attachments, Generation and Manage tabs
- 100 MB upload and 100,000-character extraction limits
- Automatic database migration from v3; history remains in `%USERPROFILE%\.peabox_streamlit_llm`

## Run
Double-click `run_windows.bat`. No administrator rights or PowerShell activation is required. Open Settings first, save/test a provider, then return to Chat and discover models.

## Security
API keys remain in Windows Credential Manager via `keyring`; non-secret settings remain in `config.json`. This is a single-user local application, not a hardened multi-user service.
