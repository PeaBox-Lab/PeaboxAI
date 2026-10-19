A local-first, multi-provider LLM workbench for chatting with local, remote and cloud AI models. 
Built with Streamlit for Ollama, OpenAI, Anthropic, Gemini, Groq, OpenRouter, LiteLLM and OpenAI-compatible AI models.

# 🟣 PeaBox LLM Workbench

**One workbench for local, remote, and cloud AI models.**

PeaBox LLM Workbench is a local-first, multi-provider AI workspace built with Streamlit. It provides a single interface for working with Ollama, OpenAI, Anthropic, Gemini, Groq, OpenRouter, LiteLLM, Open WebUI, LM Studio, and other OpenAI-compatible endpoints.

Instead of switching between different AI applications, provider dashboards, and local-model interfaces, PeaBox gives you one workspace for conversations, models, files, vision inputs, reasoning controls, and provider configuration.

> **v4.0.0 – Multi-Provider Workbench**

---

## ✨ Why PeaBox?

Running different LLMs usually means using different applications.

You might have:

- Ollama running locally
- Ollama running on a remote server
- OpenAI for one task
- Claude for another
- Gemini for another
- Groq or OpenRouter for experimentation
- LiteLLM acting as a common gateway
- LM Studio for local models

PeaBox brings these environments together.

```text
                    PeaBox LLM Workbench
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
      Local               Remote              Cloud
        │                   │                   │
      Ollama           SSH Ollama        OpenAI / Claude
    LM Studio            LiteLLM         Gemini / Groq
                                             OpenRouter
```

The goal is simple:

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

You can switch providers and models without changing applications.

---

## 🏠 Local Ollama

Connect directly to an Ollama server running on your computer.

Example:

```text
Provider: Direct Ollama
Base URL: http://localhost:11434
```

PeaBox can discover the models available through the configured Ollama server.

Typical examples might include models you have installed locally such as:

```text
qwen
llama
mistral
deepseek
gemma
```

The actual model list depends on your Ollama installation.

---

## 🌐 Remote Ollama over SSH

PeaBox can also communicate with Ollama running on another machine through SSH.

This is useful when your models are running on:

- another workstation
- a Linux VM
- a home lab
- AWS
- Oracle Cloud
- Azure VM
- other remote infrastructure

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

This allows the Ollama service itself to remain bound to the remote machine while PeaBox communicates with it through SSH.

---

# ☁️ Cloud AI Providers

PeaBox can connect to cloud-hosted LLM APIs.

Examples include:

```text
OpenAI
Anthropic
Google Gemini
Groq
OpenRouter
Mistral
Together AI
```

PeaBox also supports OpenAI-compatible APIs, making it possible to connect additional gateways and inference servers without requiring a dedicated provider implementation for every service.

---

# 🔌 OpenAI-Compatible Endpoints

A major part of PeaBox is its support for OpenAI-compatible APIs.

Example:

```text
Provider:
OpenAI-compatible

Base URL:
http://localhost:4000/v1

Model:
your-model-name
```

This makes PeaBox useful with tools such as:

```text
LiteLLM
LM Studio
OpenRouter
Groq
custom gateways
self-hosted inference endpoints
```

---

# 🧭 Model Discovery

PeaBox can discover models exposed by supported providers.

From the Workbench:

```text
Discover / Refresh Models
```

The application retrieves the available model list and makes those models available for selection.

This is particularly useful when experimenting with local models because your installed model collection can change frequently.

---

# 💬 Persistent Conversations

Conversations are stored locally using SQLite.

PeaBox supports:

- New conversations
- Conversation history
- Reopening previous conversations
- Conversation titles
- Renaming
- Pinning
- Archiving
- Deleting conversations
- JSON conversation export

Your conversations remain available after restarting the Workbench.

---

# 📎 File Attachments

PeaBox can use uploaded documents as additional context for your conversation.

Supported formats include:

### Documents

```text
PDF
DOCX
PPTX
```

### Spreadsheets and data

```text
XLSX
XLSM
CSV
JSON
```

### Text and markup

```text
TXT
Markdown
XML
HTML
YAML
```

### Source code

Examples include:

```text
Python
JavaScript
TypeScript
PowerShell
HTML
CSS
configuration files
logs
```

PeaBox extracts supported text content and adds it to the conversation context.

---

# 👁️ Vision Support

PeaBox can send images to compatible vision models.

Supported image uploads include:

```text
PNG
JPG
JPEG
WEBP
```

If the selected model is recognized as vision-capable, images can be included alongside the user prompt.

This makes PeaBox useful for tasks such as:

- screenshot analysis
- UI review
- diagram understanding
- document-image analysis
- visual debugging

Vision capability depends on the selected model/provider.

---

# 🧠 Reasoning Controls

For models that support reasoning or thinking behaviour, PeaBox exposes reasoning controls.

Depending on the model, options can include:

```text
Default
Off
Low
Medium
High
Max
```

This lets you use lighter reasoning for simple requests and stronger reasoning for more complex analysis where supported.

---

# 🎛️ Generation Controls

PeaBox exposes commonly used model-generation parameters.

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

You can also choose:

```text
Use Model Defaults
```

when you do not want PeaBox to override the model's own defaults.

Not every parameter is supported by every provider.

---

# ⚙️ Settings & API Vault

Provider configuration is kept separate from the primary chat workspace.

Open:

```text
Settings & API Vault
```

From here you can configure AI connections such as:

```text
Provider
Base URL
API Key
Default Model
SSH Host
SSH User
SSH Port
Private Key
```

You can also:

- enable or disable providers
- save provider configuration
- test connections
- discover models
- select preferred models

Keeping configuration away from the main chat interface helps keep the day-to-day workspace focused.

---

# 🔐 API Key Storage

PeaBox uses the operating system credential store through Python's `keyring` package for provider credentials.

On Windows, credentials are kept outside the application's normal configuration file.

Non-secret configuration and conversation data are stored separately.

You should never commit:

```text
API keys
SSH private keys
credential exports
.env files containing secrets
```

to your Git repository.

---

# 🗂️ Application Layout

The v4 interface is organized around four primary areas:

```text
PeaBox LLM Workbench

├── Chat
│   ├── Conversation history
│   ├── Provider
│   ├── Model
│   └── Responses
│
├── Attachments
│   ├── Documents
│   ├── Spreadsheets
│   ├── Code
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
    ├── API credentials
    ├── Endpoints
    ├── Model discovery
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

Main Streamlit Workbench interface.

Handles:

- chat UI
- conversations
- provider/model selection
- attachments
- generation settings
- response display

### `providers.py`

Provider abstraction layer.

Handles connections to:

- Ollama
- SSH Ollama
- OpenAI-compatible APIs
- Anthropic
- cloud providers

It also manages model discovery and provider-specific requests.

### `attachments.py`

Extracts usable content from supported uploaded files.

### `storage.py`

Handles:

- SQLite database
- conversations
- messages
- application configuration

### `pages/1_Settings.py`

Dedicated provider configuration and API-management interface.

---

# 🗄️ Local Data Storage

PeaBox stores application data under the user's local profile.

On Windows:

```text
%USERPROFILE%\.peabox_streamlit_llm
```

Typical content includes:

```text
workbench.db
config.json
```

### `workbench.db`

SQLite database containing conversation history and related application data.

### `config.json`

Non-secret application/provider configuration.

Credentials are kept separately using the operating system credential mechanism.

---

# 📦 Installation

## Requirements

You need:

```text
Windows
Python 3
Internet access for cloud providers
```

If you want local Ollama models, install and configure Ollama separately.

If you want SSH Ollama, you also need access to a remote machine running Ollama and a valid SSH configuration.

---

# 🪟 Windows Quick Start

Download or clone the repository.

Open the project directory and double-click:

```text
run_windows.bat
```

The launcher creates the Python environment when necessary, installs dependencies, and starts Streamlit.

No manual PowerShell virtual-environment activation is required.

---

# 🐍 Manual Installation

Create a virtual environment:

```powershell
py -m venv .venv
```

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Start PeaBox:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Streamlit will display the local Workbench URL after startup.

---

# 🦙 Configure Ollama

For an Ollama server running on your machine:

```text
Provider:
Direct Ollama
```

Set:

```text
Base URL:
http://localhost:11434
```

Then use:

```text
Discover / Refresh Models
```

to retrieve the available model list.

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

Save the configuration and test connectivity.

PeaBox can then communicate with the Ollama instance through SSH.

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

Then configure:

```text
API Key
Default Model
```

according to your LiteLLM setup.

Because LiteLLM provides an OpenAI-compatible interface, it can also be used as a common gateway between PeaBox and multiple underlying LLM providers.

---

# 🧪 Configure LM Studio

Start the local server from LM Studio.

Then configure PeaBox with the endpoint displayed by your LM Studio server.

A commonly used local OpenAI-compatible base URL is:

```text
http://localhost:1234/v1
```

Use the actual address shown by your installation.

---

# 🔑 Configure Cloud Providers

Open:

```text
Settings & API Vault
```

Choose your provider and configure:

```text
API Key
Base URL
Default Model
```

Save the connection.

Then:

```text
Test Connection
```

or:

```text
Discover Models
```

before returning to the chat workspace.

---

# 📝 First Run

A good first-run flow is:

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

# 🔄 Switching Models

PeaBox is designed for experimentation.

You can move between:

```text
Local model
     ↓
Remote model
     ↓
Cloud model
     ↓
Another provider
```

without changing applications.

For example:

```text
Coding
→ local Qwen model

Detailed reasoning
→ Claude

General-purpose work
→ OpenAI model

Fast experiment
→ Groq

Model routing
→ LiteLLM
```

The right model remains your choice.

---

# 📚 Working With Documents

Open the **Attachments** tab.

Upload one or more supported documents.

Then ask questions such as:

```text
Summarize these documents.
```

```text
Compare these two files.
```

```text
Identify differences between these requirements.
```

```text
Create action items from this document.
```

```text
Explain this source code.
```

```text
Analyse this spreadsheet.
```

Document content is added to the model context subject to the Workbench's extraction limits.

---

# 💻 Using PeaBox With Code

You can upload supported source files and ask the selected model to:

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

PeaBox v4 does **not** automatically execute generated code.

---

# 🛡️ Security Considerations

PeaBox is designed primarily as a local, single-user Workbench.

Keep the following in mind:

### API credentials

Do not store API keys directly in source files.

### SSH keys

Never add SSH private keys to the repository.

### `.gitignore`

Ensure local runtime files and credentials are excluded.

Recommended entries:

```gitignore
.venv/
__pycache__/
*.pyc
.env

.peabox/
.peabox_stream*it_llm/

.streamlit/secrets.toml

*.key
*.pem
```

### Uploaded documents

*ocuments sent*to a cloud LLM may leave your comp*ter.

If information is sensitive,*consider using:

```text
Local Oll*ma
```

or another appropriately c*ntrolled local/self-hosted model i*stead.

---

# 🔒 Privacy Model

P*aBox can operate*with different privacy models*depending on the selected provider*

```text
Local Ollama
      │
   *  └── Local processing

Remote Oll*ma
      │
      └── Your remote i*frastructure

Cloud API
      │
  *   └── External AI provider
```

T*e privacy and data-handling rules *f the selected model provider stil* apply.

PeaBox itself does not ma*e an external cloud model local si*ply by providing a local interface*

---

# ❓ Troubleshooting

## No *llama models appear

Check whether*Ollama is running.

Also verify th* configured base URL:

```text
htt*://localhost:11434
```

Then refre*h model discovery.

---

## Remote*Ollama fails

Check:

```text
SSH *ost
SSH username
SSH port
Private-*ey path
Remote Ollama process
```
*Try connecting to the machine usin* your normal SSH client first.

--*

## API provider fails

Verify:

*``text
API key
Base URL
Model name*Account/provider access
Network co*nectivity
```

Use the connection-*est option in Settings.

---

## P*thon dependency problem

Reinstall*dependencies:

```powershell
*\.venv\Scripts\python.exe -m pip i*stall --upgrade pip
.\.venv\Script*\python.exe -m pip install -r requ*rements.txt
```

---

## Start wit* a clean virtual environment

Dele*e:

```text
.venv
```

Then run:

*``text
run_windows.bat
```

again.*
Your conversation database is sto*ed separately from the project vir*ual environment.

---

# 🗺️ Produ*t Direction

v4 establishes PeaBox*as a multi-provider AI Workbench.
*Natural areas for future developme*t include:

```text
Projects / Wor*spaces
Persistent Knowledge
Prompt*Library
Model Compare
Streaming
Re*earch Mode
Usage & Cost Analytics
*rtifacts
Model Benchmarking
Tool C*lling
Local Data Analysis
Backup /*Restore
```

The longer-term idea *s to move PeaBox beyond a multi-LL* chat client toward a broader AI p*oductivity workbench.

---

# 🤝 C*ntributing

Contributions are welc*me.

Good contribution areas inclu*e:

- additional provider adapters*- attachment processors
- Streamli* UI improvements
- model-discovery*improvements
- conversation-manage*ent features
- documentation
- tes*s
- accessibility
- performance im*rovements

A typical contribution *orkflow:

```bash
git clone <your-*epository-url>
cd PeaBox-LLM-Workb*nch

git checkout -b feature/my-fe*ture
```

Make your changes, test *hem locally, then submit a pull re*uest.

Please avoid committing:

`*`text
API keys
SSH credentials
per*onal configuration
conversation da*abases
private documents
```

---
*# 🐛 Issues

When reporting a prob*em, include:

```text
PeaBox versi*n
Python version
Operating system
*rovider
Model
Relevant error messa*e
Steps to reproduce
```

Please r*move:

```text
API keys
tokens
pas*words
SSH credentials
private host*ames/IPs
sensitive document conten*
```

before posting logs or scree*shots.

---

# 💡 Feature Requests*
Feature ideas are welcome.

Usefu* requests should explain:

1. The *roblem
2. The intended workflow
3.*Why the feature belongs in PeaBox
*. Which providers/models it affect*
5. An example use case

---

# 📜*License

Add an open-source licens* before publishing or distributing*the project.

If PeaBox is release* under Apache License 2.0, place t*e full license text in:

```text
L*CENSE
```

and update this section*to:

```text
Licensed under the Ap*che License 2.0.
```

Do not adver*ise a license until the correspond*ng `LICENSE` file has actually bee* added to the repository.

---

# *� About PeaBox

PeaBox is built ar*und a simple idea:

**small experi*ents can grow into useful tools.***
Each experiment is a pea.

PeaBox*is where those ideas come together* evolve, and become something usef*l.

PeaBox LLM Workbench is one of*those experiments: a practical env*ronment for exploring local models* cloud AI, self-hosted infrastruct*re, and different ways of working *ith LLMs.

---

## ⭐ Support the P*oject

If PeaBox LLM Workbench is *seful to you:

- ⭐ Star the reposi*ory
- 🐛 Report issues
- 💡 Sugges* features
- 🔧 Contribute improvem*nts
- 🍴 Fork and experiment

---
*## PeaBox LLM Workbench

**Your*models* Your APIs. One AI workbench.**

B*ilt for*people who want the freedom to cho*se*where and*how their AI runs.
````*
