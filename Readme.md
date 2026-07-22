# RAG Knowledge Assistant
### *Intelligent Open-Source & Dependency Auditing Dashboard*

**Team Name:** Hi-Five Agents

---

## Overview

RAG Knowledge Assistant is a Streamlit-based dashboard that helps developers assess whether an open-source package is **safe to add to their codebase**. Ask a question about any package (e.g. *"Is `left-pad` safe to add to our repo?"*), and the assistant combines:

-  **Local compliance knowledge** (via a Retrieval-Augmented Generation index)
-  **GitHub repository health metrics** (stars, forks, issues, commit activity, releases)
-  **Live web search** for recent bug/vulnerability reports
-  **Google Gemini synthesis** to generate a structured risk report

...and returns a clear, actionable risk assessment in a chat-style interface.

---

## Features

- **Chat-style UI** for natural, conversational package queries
- **Secure sidebar inputs** for API keys (GitHub, Serper, Gemini) — session-only, never written to disk
- **Cached RAG pipeline** using LlamaIndex + local Hugging Face embeddings, so the index is built once per session
- **GitHub telemetry** — stars, forks, open/closed issues, commits in the last 30 days, recent releases, archived status
- **Web search integration** via Serper (Google Search API) for community threat notices
- **Documentation scraping** with SSRF-safe domain allow-listing (PyPI, ReadTheDocs, GitHub)
- **AI-generated risk reports** with consistent structure:
  - Summary
  - Security Risks
  - Maintenance Status
  - Community Popularity
  - Recommendation
  - Risk Score (0–10)

---

## Architecture

```
User Query (Streamlit Chat)
        │
        ├──► rag/loader.py           → Load local compliance documents
        ├──► rag/storage_manager.py  → Build/load vector index (cached)
        ├──► rag/retriever.py        → Retrieve relevant compliance context
        │
        ├──► github_matrix.py        → Fetch live GitHub repo metrics
        ├──► search_engine.py        → Serper web search + doc scraping
        │
        └──► rag/ai_assistant.py     → Gemini synthesizes final report
                        │
                        ▼
              Risk Assessment Report
```

---

## Project Structure

```
.
├── app.py                  # Streamlit UI, session state, orchestration
├── github_matrix.py        # GitHub API metrics (stars, issues, forks, releases)
├── search_engine.py        # Serper search + documentation scraper
├── requirements.txt        # Python dependencies
│
├── rag/
│   ├── __init__.py         # Configures global embedding model (Settings)
│   ├── config.py           # Embedding model, chunk size, storage dir, top_k
│   ├── loader.py           # Loads documents from data/uploads
│   ├── indexer.py          # Builds the vector index from documents
│   ├── storage_manager.py  # Loads existing index or builds a new one
│   ├── retriever.py        # Returns a configured retriever
│   ├── ai_assistant.py     # GeminiAssistant — generates the audit report
│   └── report_generator.py # Thin wrapper around GeminiAssistant
│
├── test_ai.py               # Sanity test for GeminiAssistant
├── test_report.py           # Sanity test for ReportGenerator
└── demo.txt                 # Sample document for testing the RAG pipeline
```

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd <your-repo-name>
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the project root:
```env
GITHUB_TOKEN=your_github_token_here
GEMINI_API_KEY=your_gemini_api_key_here
```
> Note: The Serper API key is entered directly in the app's sidebar at runtime and is not required in `.env`.

### 5. Run the app
```bash
streamlit run app.py
```

---

## API Keys Required

| Key | Purpose | Where to get it |
|---|---|---|
| **GitHub Token** | Fetch repo stars, issues, forks, commit activity | [github.com/settings/tokens](https://github.com/settings/tokens) |
| **Serper API Key** | Google Search results for vulnerability/bug notices | [serper.dev](https://serper.dev) |
| **Gemini API Key** | Synthesizes the final risk report | [Google AI Studio](https://aistudio.google.com/) |

Enter all three keys in the sidebar and click **"Save & Initialize"** before starting a query.

---

## Testing

Quick sanity checks for the AI report generation pipeline:
```bash
python test_ai.py        # Tests GeminiAssistant.generate_report() directly
python test_report.py    # Tests the ReportGenerator wrapper
```

---

## Tech Stack

- **Frontend:** Streamlit
- **RAG / Indexing:** LlamaIndex, Hugging Face Sentence Transformers (`BAAI/bge-small-en-v1.5`)
- **LLM Synthesis:** Google Gemini (`gemini-2.5-flash`)
- **External Data:** GitHub REST API, Serper (Google Search API)
- **Language:** Python

---

## Team — Hi-Five Agents

| Role | Responsibility |
|---|---|
| Frontend Architect & UI Lead | Streamlit layout, sidebar, chat UI, session state |
| RAG Engineer | LlamaIndex pipeline, embeddings, retriever, storage |
| GitHub Metrics Engineer | `github_matrix.py` — repo health telemetry |
| Search Engineer | `search_engine.py` — Serper search & doc scraping |
| AI Synthesis Engineer | `ai_assistant.py` — Gemini prompt design & report generation |

---

## Notes

- Local compliance data lives in `data/uploads/` and is indexed once, then cached for the session.
- API keys are session-scoped only and are never persisted to disk.
- The web scraper enforces a domain allow-list (`pypi.org`, `readthedocs.io/org`, `github.com`) to prevent SSRF.

---

*Built by Team Hi-Five Agents*# 🔎 RAG Knowledge Assistant
### *Intelligent Open-Source & Dependency Auditing Dashboard*

**Team Name:** Hi-Five Agents

🚀 **Live App:** [hi-five-agents.streamlit.app](https://hi-five-agents.streamlit.app/)

---

## 📖 Overview

RAG Knowledge Assistant is a Streamlit-based dashboard that helps developers assess whether an open-source package is **safe to add to their codebase**. Ask a question about any package (e.g. *"Is `left-pad` safe to add to our repo?"*), and the assistant combines:

- **Local compliance knowledge** (via a Retrieval-Augmented Generation index)
- **GitHub repository health metrics** (stars, forks, issues, commit activity, releases)
- **Live web search** for recent bug/vulnerability reports
- **Google Gemini synthesis** to generate a structured risk report

...and returns a clear, actionable risk assessment in a chat-style interface.

---

## Features

- **Chat-style UI** for natural, conversational package queries
- **Secure sidebar inputs** for API keys (GitHub, Serper, Gemini) — session-only, never written to disk
- **Cached RAG pipeline** using LlamaIndex + local Hugging Face embeddings, so the index is built once per session
- **GitHub telemetry** — stars, forks, open/closed issues, commits in the last 30 days, recent releases, archived status
- **Web search integration** via Serper (Google Search API) for community threat notices
- **Documentation scraping** with SSRF-safe domain allow-listing (PyPI, ReadTheDocs, GitHub)
- **AI-generated risk reports** with consistent structure:
  - Summary
  - Security Risks
  - Maintenance Status
  - Community Popularity
  - Recommendation
  - Risk Score (0–10)

---

## Architecture

```
User Query (Streamlit Chat)
        │
        ├──► rag/loader.py           → Load local compliance documents
        ├──► rag/storage_manager.py  → Build/load vector index (cached)
        ├──► rag/retriever.py        → Retrieve relevant compliance context
        │
        ├──► github_matrix.py        → Fetch live GitHub repo metrics
        ├──► search_engine.py        → Serper web search + doc scraping
        │
        └──► rag/ai_assistant.py     → Gemini synthesizes final report
                        │
                        ▼
              Risk Assessment Report
```

---

## Project Structure

```
.
├── app.py                  # Streamlit UI, session state, orchestration
├── github_matrix.py        # GitHub API metrics (stars, issues, forks, releases)
├── search_engine.py        # Serper search + documentation scraper
├── requirements.txt        # Python dependencies
│
├── rag/
│   ├── __init__.py         # Configures global embedding model (Settings)
│   ├── config.py           # Embedding model, chunk size, storage dir, top_k
│   ├── loader.py           # Loads documents from data/uploads
│   ├── indexer.py          # Builds the vector index from documents
│   ├── storage_manager.py  # Loads existing index or builds a new one
│   ├── retriever.py        # Returns a configured retriever
│   ├── ai_assistant.py     # GeminiAssistant — generates the audit report
│   └── report_generator.py # Thin wrapper around GeminiAssistant
│
├── test_ai.py               # Sanity test for GeminiAssistant
├── test_report.py           # Sanity test for ReportGenerator
└── demo.txt                 # Sample document for testing the RAG pipeline
```

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd <your-repo-name>
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the project root:
```env
GITHUB_TOKEN=your_github_token_here
GEMINI_API_KEY=your_gemini_api_key_here
```
> Note: The Serper API key is entered directly in the app's sidebar at runtime and is not required in `.env`.

### 5. Run the app
```bash
streamlit run app.py
```

---

## API Keys Required

| Key | Purpose | Where to get it |
|---|---|---|
| **GitHub Token** | Fetch repo stars, issues, forks, commit activity | [github.com/settings/tokens](https://github.com/settings/tokens) |
| **Serper API Key** | Google Search results for vulnerability/bug notices | [serper.dev](https://serper.dev) |
| **Gemini API Key** | Synthesizes the final risk report | [Google AI Studio](https://aistudio.google.com/) |

Enter all three keys in the sidebar and click **"Save & Initialize"** before starting a query.

---

## Testing

Quick sanity checks for the AI report generation pipeline:
```bash
python test_ai.py        # Tests GeminiAssistant.generate_report() directly
python test_report.py    # Tests the ReportGenerator wrapper
```

---

## Tech Stack

- **Frontend:** Streamlit
- **RAG / Indexing:** LlamaIndex, Hugging Face Sentence Transformers (`BAAI/bge-small-en-v1.5`)
- **LLM Synthesis:** Google Gemini (`gemini-2.5-flash`)
- **External Data:** GitHub REST API, Serper (Google Search API)
- **Language:** Python

---

## Team — Hi-Five Agents

| Role | Responsibility |
|---|---|
| Frontend Architect & UI Lead | Streamlit layout, sidebar, chat UI, session state |
| RAG Engineer | LlamaIndex pipeline, embeddings, retriever, storage |
| GitHub Metrics Engineer | `github_matrix.py` — repo health telemetry |
| Search Engineer | `search_engine.py` — Serper search & doc scraping |
| AI Synthesis Engineer | `ai_assistant.py` — Gemini prompt design & report generation |

---

## Notes

- Local compliance data lives in `data/uploads/` and is indexed once, then cached for the session.
- API keys are session-scoped only and are never persisted to disk.
- The web scraper enforces a domain allow-list (`pypi.org`, `readthedocs.io/org`, `github.com`) to prevent SSRF.

---

*Built by Team Hi-Five Agents*