A local-first, multi-provider LLM workbench for chatting with local, remote and cloud AI models. 
Built with Streamlit for Ollama, OpenAI, Anthropic, Gemini, Groq, OpenRouter, LiteLLM and OpenAI-compatible AI models.

# 🟣 PeaBox LLM Workbench

**One workbench for local, remote, and cloud AI models.**

PeaBox LLM Workbench is a local-first, multi-provider AI workspace built with Streamlit. It provides a single interface for working with Ollama, OpenAI, Anthropic, Google Gemini, Groq, OpenRouter, LiteLLM, Open WebUI, LM Studio, and other OpenAI-compatible endpoints.

Instead of switching between different AI applications, provider dashboards, and local model interfaces, PeaBox gives you one workspace for conversations, model selection, files, vision inputs, reasoning controls, and provider configuration.

> **v4.0.0 – Multi-Provider Workbench**

---

## ✨ Why PeaBox?

Working with different LLMs often means using different applications.

You might have:

- Ollama running locally
- Ollama running on a remote server
- OpenAI for one task
- Claude for another
- Gemini for another
- Groq or OpenRouter for experimentation
- LiteLLM acting as a common gateway
- LM Studio running local models

PeaBox brings these environments together.

```text
                     PeaBox LLM Workbench
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
        Local              Remote             Cloud
          │                  │                  │
       Ollama           SSH Ollama       OpenAI / Claude
     LM Studio            LiteLLM        Gemini / Groq
                                           OpenRouter
```

The idea is simple:

> **Your models. Your APIs. One AI workbench.**

---

# 🚀 Features

## 🤖 Multi-Provider AI

PeaBox provides one interface for multiple LLM providers and runtimes.

Supported connection types include:

- Ollama
- Remote Ollama over SSH
- OpenAI
- Anthropic
- Google Gemini
- Groq
- OpenRouter
- LiteLLM
- LM Studio
- Open WebUI
- Custom OpenAI-compatible endpoints

You can switch between providers and models without changing applications.

---

## 🏠 Local Ollama

Connect directly to an Ollama server running on your computer.

Example:

```text
Provider: Direct Ollama
Base URL: http://localhost:11434
```

PeaBox can discover models available through the configured Ollama server.

Your model list depends on the models installed in your local Ollama environment.

---

## 🌐 Remote Ollama over SSH

PeaBox can communicate with Ollama running on another machine through SSH.

This is useful when your models are running on:

- Another workstation
- A Linux VM
- A home lab
- AWS
- Oracle Cloud
- Azure VM
- Other remote infrastructure

Example configuration:

```text
Provider: SSH Ollama

Host:
192.168.x.x

SSH User:
opc

SSH Port:
22

Private Key:
C:\Users\YourName\.ssh\server.key
```

This allows Ollama to remain on the remote machine while PeaBox communicates with it securely through SSH.

---

# ☁️ Cloud AI Providers

PeaBox can connect to cloud-hosted LLM APIs.

Supported services include:

- OpenAI
- Anthropic
- Google Gemini
- Groq
- OpenRouter
- Mistral
- Together AI

PeaBox also supports OpenAI-compatible APIs, allowing you to connect additional gateways and inference servers without requiring a dedicated implementation for every provider.

---

# 🔌 OpenAI-Compatible Endpoints

A major feature of PeaBox is support for OpenAI-compatible APIs.

Example:

```text
Provider:
OpenAI-compatible

Base URL:
http://localhost:4000/v1

Model:
your-model-name
```

This makes PeaBox suitable for tools and services such as:

- LiteLLM
- LM Studio
- OpenRouter
- Groq
- Custom gateways
- Self-hosted inference endpoints

---

# 🧭 Model Discovery

PeaBox can discover models exposed by supported providers.

From the Workbench, select:

```text
Discover / Refresh Models
```

The application retrieves the available model list and makes those models available for selection.

This is especially useful when experimenting with local models because your installed model collection may change frequently.

---

# 💬 Persistent Conversations

Conversations are stored locally using SQLite.

PeaBox supports:

- Creating new conversations
- Conversation history
- Reopening previous conversations
- Automatic conversation titles
- Renaming conversations
- Pinning conversations
- Archiving conversations
- Deleting conversations
- Exporting conversations as JSON

Your conversation history remains available after restarting the Workbench.

---

# 📎 File Attachments

PeaBox can use uploaded files as additional context for your conversations.

## Documents

```text
PDF
DOCX
PPTX
```

## Spreadsheets and Data

```text
XLSX
XLSM
CSV
JSON
```

## Text and Markup

```text
TXT
Markdown
XML
HTML
YAML
YML
```

## Source Code and Technical Files

Examples include:

```text
Python
JavaScript
TypeScript
PowerShell
HTML
Configuration files
Log files
```

PeaBox extracts supported textual content and adds it to the conversation context.

---

# 👁️ Vision Support

PeaBox can send images to compatible vision models.

Supported image formats include:

```text
PNG
JPG
JPEG
WEBP
```

If the selected model supports vision, images can be included alongside the user's prompt.

This can be useful for:

- Screenshot analysis
- UI reviews
- Diagram analysis
- Document image analysis
- Visual debugging
- Image-based questions

Vision capabilities depend on the selected model and provider.

---

# 🧠 Reasoning Controls

For models that support reasoning or thinking capabilities, PeaBox provides reasoning controls.

Depending on the selected model, available options can include:

```text
Default
Off
Low
Medium
High
Max
```

This allows you to use lighter reasoning for straightforward requests and higher reasoning levels for more complex tasks where the model supports them.

---

# 🎛️ Generation Controls

PeaBox provides access to commonly used generation parameters.

These include:

```text
Temperature
Top P
Top K
Repeat Penalty
Context Tokens
Maximum Output Tokens
Reasoning Level
```

You can also select:

```text
Use Model Defaults
```

when you want the model or provider to control its own generation settings.

Not every parameter is supported by every provider or model.

---

# ⚙️ Settings & API Vault

Provider configuration is separated from the main chat workspace.

Open:

```text
Settings & API Vault
```

From here, you can configure connections using settings such as:

```text
Provider
Base URL
API Key
Default Model
SSH Host
SSH User
SSH Port
Private Key Path
```

You can also:

- Enable or disable providers
- Save provider configurations
- Test connections
- Discover available models
- Configure preferred models

Keeping provider configuration separate from the main interface keeps the day-to-day chat workspace clean and focused.

---

# 🔐 API Key Storage

PeaBox uses the operating system's credential store through Python's `keyring` package for provider credentials.

On Windows, API credentials are stored outside the application's regular configuration files.

Non-sensitive configuration and conversation data are stored separately.

Never commit the following to a Git repository:

```text
API keys
SSH private keys
Passwords
Credential exports
.env files containing secrets
```

---

# 🗂️ Application Layout

The v4 interface is organized around four primary areas:

```text
PeaBox LLM Workbench

├── Chat
│   ├── Conversation History
│   ├── Provider Selection
│   ├── Model Selection
│   └── AI Responses
│
├── Attachments
│   ├── Documents
│   ├── Spreadsheets
│   ├── Source Code
│   └── Images
│
├── Generation
│   ├── Temperature
│   ├── Top P
│   ├── Top K
│   ├── Context
│   └── Reasoning
│
└── Settings & API Vault
    ├── Providers
    ├── API Credentials
    ├── Endpoints
    ├── Model Discovery
    └── Defaults
```

---

# 📁 Project Structure

A typical v4 installation looks like this:

```text
PeaBox-LLM-Workbench/
│
├── app.py
├── providers.py
├── attachments.py
├── storage.py
├── requirements.txt
├── run_windows.bat
├── README.md
│
├── pages/
│   └── 1_Settings.py
│
└── .streamlit/
    └── config.toml
```

### `app.py`

The main Streamlit Workbench interface.

It handles:

- Chat UI
- Conversation management
- Provider and model selection
- Attachments
- Generation settings
- AI response display

### `providers.py`

The provider abstraction layer.

It handles connections to:

- Ollama
- Remote Ollama over SSH
- OpenAI-compatible APIs
- Anthropic
- Supported cloud providers

It also handles model discovery and provider-specific requests.

### `attachments.py`

Processes supported uploaded files and extracts usable content.

### `storage.py`

Handles:

- SQLite database operations
- Conversations
- Messages
- Application configuration

### `pages/1_Settings.py`

Provides the dedicated provider configuration and API management interface.

---

# 🗄️ Local Data Storage

PeaBox stores application data under the user's local profile.

On Windows:

```text
%USERPROFILE%\.peabox_streamlit_llm
```

Typical files include:

```text
workbench.db
config.json
```

## `workbench.db`

The SQLite database used for conversation history and related application data.

## `config.json`

Stores non-sensitive application and provider configuration.

Credentials are stored separately using the operating system's credential storage mechanism.

---

# 📦 Installation

## Requirements

You need:

- Windows
- Python 3
- Internet access when using cloud providers

If you want to use local Ollama models, install and configure Ollama separately.

If you want to use remote Ollama over SSH, you will also need access to a remote machine running Ollama and a valid SSH configuration.

---

# 🪟 Windows Quick Start

Download or clone the repository.

Open the project directory and double-click:

```text
run_windows.bat
```

The launcher creates the Python virtual environment when required, installs the necessary dependencies, and starts the Streamlit application.

No manual PowerShell virtual environment activation is required.

---

# 🐍 Manual Installation

Create a virtual environment:

```powershell
py -m venv .venv
```

Install the dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Start PeaBox:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Streamlit will display the local Workbench address after startup.

---

# 🦙 Configure Ollama

For an Ollama server running locally:

```text
Provider:
Direct Ollama
```

Set:

```text
Base URL:
http://localhost:11434
```

Then select:

```text
Discover / Refresh Models
```

to retrieve the available models.

---

# 🖥️ Configure Remote Ollama

Open:

```text
Settings & API Vault
```

Select:

```text
SSH Ollama
```

Configure:

```text
Host
SSH User
SSH Port
Private Key Path
```

Save the configuration and test the connection.

PeaBox can then communicate with the remote Ollama instance through SSH.

---

# 🔗 Configure LiteLLM

Select:

```text
LiteLLM
```

Example endpoint:

```text
http://localhost:4000/v1
```

Configure:

```text
API Key
Default Model
```

according to your LiteLLM setup.

Because LiteLLM provides an OpenAI-compatible interface, it can act as a common gateway between PeaBox and multiple underlying LLM providers.

---

# 🧪 Configure LM Studio

Start the local server from LM Studio.

Configure PeaBox using the OpenAI-compatible endpoint displayed by LM Studio.

For example:

```text
http://localhost:1234/v1
```

Use the actual address displayed by your LM Studio installation.

---

# 🔑 Configure Cloud Providers

Open:

```text
Settings & API Vault
```

Choose the required provider and configure:

```text
API Key
Base URL
Default Model
```

Save the connection.

Then use:

```text
Test Connection
```

or:

```text
Discover Models
```

before returning to the main chat workspace.

---

# 📝 First Run

A typical first-run workflow is:

```text
1. Start PeaBox
        ↓
2. Open Settings & API Vault
        ↓
3. Configure a provider
        ↓
4. Save the connection
        ↓
5. Test the connection
        ↓
6. Return to Chat
        ↓
7. Discover models
        ↓
8. Select a model
        ↓
9. Start chatting
```

---

# 🔄 Switching Between Models

PeaBox is designed for experimentation.

You can move between:

```text
Local Model
     ↓
Remote Model
     ↓
Cloud Model
     ↓
Another Provider
```

without changing applications.

For example:

```text
Coding
→ Local coding model

Detailed reasoning
→ Reasoning-capable model

General-purpose work
→ General-purpose cloud model

Fast experimentation
→ Low-latency provider

Model routing
→ LiteLLM
```

The model remains your choice.

---

# 📚 Working With Documents

Open the **Attachments** tab.

Upload one or more supported documents.

You can then ask questions such as:

```text
Summarize these documents.
```

```text
Compare these two files.
```

```text
Identify the differences between these requirements.
```

```text
Create action items from this document.
```

```text
Explain this source code.
```

```text
Analyze this spreadsheet.
```

Document content is added to the model context, subject to the Workbench's extraction limits.

---

# 💻 Working With Code

Upload supported source files and ask the selected model to:

```text
Explain this code.
```

```text
Find potential bugs.
```

```text
Refactor this function.
```

```text
Generate unit tests.
```

```text
Convert this implementation to another language.
```

```text
Explain the architecture.
```

PeaBox v4 does not automatically execute generated code.

---

# 🛡️ Security Considerations

PeaBox is designed primarily as a local, single-user Workbench.

Keep the following points in mind.

## API Credentials

Do not store API keys directly in source files.

## SSH Keys

Never add SSH private keys to the repository.

## `.gitignore`

Make sure that local runtime files and credentials are excluded.

Recommended entries:

```gitignore
.venv/
__pycache__/
*.pyc
.env

.peabox/
.peabox_streamlit_llm/

.streamlit/secrets.toml

*.key
*.pem
```

## Uploaded Documents

Documents sent to a cloud LLM may leave your computer and be processed by an external service.

For sensitive information, consider using an appropriately controlled local or self-hosted model.

---

# 🔒 Privacy Model

PeaBox can operate with different privacy models depending on the selected provider.

```text
Local Ollama
      │
      └── Local inference

Remote Ollama
      │
      └── Your remote infrastructure

Cloud API
      │
      └── External AI provider
```

The privacy and data-handling policies of the selected model provider still apply.

Using PeaBox as a local interface does not make an external cloud model local.

---

# ❓ Troubleshooting

## Ollama Models Do Not Appear

Check whether Ollama is running.

Verify the configured base URL:

```text
http://localhost:11434
```

Then refresh model discovery.

---

## Remote Ollama Connection Fails

Check:

```text
SSH Host
SSH Username
SSH Port
Private Key Path
Remote Ollama Process
```

Try connecting to the remote machine using your normal SSH client first.

---

## Cloud Provider Connection Fails

Verify:

```text
API Key
Base URL
Model Name
Provider Access
Network Connectivity
```

Use the connection testing option in Settings.

---

## Python Dependency Problems

Upgrade `pip` and reinstall the dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## Start With a Clean Virtual Environment

Delete:

```text
.venv
```

Then run:

```text
run_windows.bat
```

again.

Your local conversation database is stored separately from the project's virtual environment.

---

# 🗺️ Product Roadmap

v4 establishes PeaBox as a multi-provider AI Workbench.

Future development areas include:

- Projects and Workspaces
- Persistent Knowledge Base
- Prompt Library
- Model Compare
- Streaming Responses
- Research Mode
- Usage and Cost Analytics
- Artifacts
- Model Benchmarking
- Tool Calling
- Local Data Analysis
- Backup and Restore

The longer-term goal is to evolve PeaBox beyond a multi-LLM chat client into a broader AI productivity Workbench.

---

# 🤝 Contributing

Contributions are welcome.

Useful contribution areas include:

- Additional provider adapters
- Attachment processors
- Streamlit UI improvements
- Model discovery improvements
- Conversation management features
- Tests
- Documentation
- Accessibility improvements
- Performance improvements

A typical contribution workflow:

```bash
git clone <your-repository-url>
cd PeaBox-LLM-Workbench

git checkout -b feature/my-feature
```

Make your changes, test them locally, and submit a pull request.

Please do not commit:

```text
API Keys
SSH Credentials
Private Keys
Personal Configuration
Conversation Databases
Private Documents
```

---

# 🐛 Reporting Issues

When reporting an issue, include:

- PeaBox version
- Python version
- Operating system
- Provider
- Model
- Relevant error message
- Steps to reproduce the issue

Before sharing logs or screenshots, remove:

```text
API Keys
Tokens
Passwords
SSH Credentials
Private Hostnames or IP Addresses
Sensitive Document Content
```

---

# 💡 Feature Requests

Feature ideas are welcome.

A useful feature request should explain:

1. The problem you are trying to solve
2. The intended workflow
3. Why the feature would be useful in PeaBox
4. Which providers or models it affects
5. An example use case

---

# 📜 License

Before publicly distributing the project as open source, add the appropriate license file to the repository.

For example, if PeaBox is released under the Apache License 2.0, add:

```text
LICENSE
```

to the root of the repository and update this section accordingly.

---

# 🟣 About PeaBox

PeaBox started with a simple idea:

**Imagine a box full of peas. Each pea is an idea or an experiment. On its own, it may be small, but when these ideas come together, they can grow into something useful.**

That is what PeaBox is about.

A place to experiment, build, learn, and turn small ideas into practical tools.

PeaBox LLM Workbench is one of those experiments: a practical workspace for exploring local models, cloud AI, self-hosted infrastructure, and different ways of working with LLMs.

---

# ⭐ Support the Project

If PeaBox LLM Workbench is useful to you:

- ⭐ Star the repository
- 🐛 Report issues
- 💡 Suggest new features
- 🔧 Contribute improvements
- 🍴 Fork it and experiment

Every contribution helps PeaBox grow.

---

# 🟣 PeaBox LLM Workbench

### **Your models. Your APIs. One AI workbench.**

Built for people who want the freedom to choose **where, how, and with which model their AI runs.**
