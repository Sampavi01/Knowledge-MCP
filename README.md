# 🚀 MCP Academic Assistant

Groq‑powered MCP chatbot with 3 servers: 🔬 Research, 📁 Filesystem, 🌐 Fetch.

## ✨ Features
- 🤖 Chat with tools (Groq `llama3-70b-8192`)
- 🔗 Multi‑server MCP (research/filesystem/fetch)
- 📚 arXiv papers: fetch, details, summarize
- 📝 Clean file writing (e.g., `results.txt`)
- 🖥️ Streamlit viewer for saved papers

## ⚡ Quick Start (copy each command one-by-one)

1) Clone
```bash
git clone https://github.com/Sampavi01/Knowledge-MCP.git
```

2) Enter folder
```bash
cd Knowledge-MCP
```

3) Create virtual env (uv)
```bash
uv venv
```

4) Activate virtual env (Windows PowerShell)
```bash
.venv\\Scripts\\activate
```

5) Activate virtual env (macOS/Linux)
```bash
source .venv/bin/activate
```

6) Install dependencies (requirements.txt)
```bash
pip install -r requirements.txt
```

7) Set API key (Windows PowerShell)
```bash
$env:GROQ_API_KEY="your_groq_api_key_here"
```

8) Set API key (macOS/Linux)
```bash
export GROQ_API_KEY=your_groq_api_key_here
```

9) Run chatbot
```bash
uv run mcp_chatbot.py
```

10) Run research server
```bash
uv run mcp_server.py
```

11) Run Streamlit UI
```bash
uv run streamlit run streamlit_app.py
```

## 📂 Structure
```
MCP Project/
├─ 🚀 mcp_chatbot.py
├─ 🔬 mcp_server.py
├─ ⚙️ server_config.json
├─ 🖥️ streamlit_app.py
├─ 📦 pyproject.toml
├─ 📚 research_papers/
└─ 📖 README.md
```

## 📝 Notes
- `research_papers/` is created when `fetch_papers(topic, limit)` runs.
- `summarize_topic(...)` returns data but doesn’t write files.
- To save text (e.g., `results.txt`), use `write_to_file` (research) or `write_file` (filesystem).

## 📄 License
MIT License. See `LICENSE` for details.
