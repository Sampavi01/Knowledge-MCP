# 🚀 MCP Academic Assistant

Groq‑powered MCP chatbot with 3 servers: 🔬 Research, 📁 Filesystem, 🌐 Fetch.

## ✨ Features
- 🤖 Chat with tools (Groq `llama3-70b-8192`)
- 🔗 Multi‑server MCP (research/filesystem/fetch)
- 📚 arXiv papers: fetch, details, summarize
- 📝 Clean file writing (e.g., `results.txt`)
- 🖥️ Streamlit viewer for saved papers

## 🎥 Demo
![MCP Chatbot Demo](ezgif.com-speed%20(2).gif)

## ⚡ Quick Start (copy each command one-by-one)
```bash
# Clone repository
git clone https://github.com/Sampavi01/Knowledge-MCP.git
# Enter project folder
cd Knowledge-MCP
```
```bash
# Create virtual environment (uv)
uv venv
# Activate venv (Windows PowerShell)
.venv\\Scripts\\activate
# Activate venv (macOS/Linux)
source .venv/bin/activate
```
```bash
# Install Python dependencies
pip install -r requirements.txt
```
```bash
# Set API key (Windows PowerShell)
$env:GROQ_API_KEY="your_groq_api_key_here"
# Set API key (macOS/Linux)
export GROQ_API_KEY=your_groq_api_key_here
```
```bash
# Run MCP chatbot
uv run mcp_chatbot.py
```
```bash
# Run research MCP server
uv run mcp_server.py
```
```bash
# Launch Streamlit UI
uv run streamlit run streamlit_app.py
```
## 📂 Structure
```
MCP Project/
├─ 🚀 mcp_chatbot.py
├─ 🔬 mcp_server.py
├─ 🤝 mcp_client.py
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
