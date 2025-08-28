# 🚀 MCP Academic Assistant

> **Multi-server MCP chatbot powered by Groq LLM for academic research & file operations**

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/MCP-Protocol-green.svg)](https://modelcontextprotocol.io)
[![Groq](https://img.shields.io/badge/LLM-Groq-orange.svg)](https://groq.com)

## ✨ What It Does

🤖 **Smart Chatbot** → Powered by Groq's llama3-70b  
🔗 **3 MCP Servers** → Research + Filesystem + Fetch  
📚 **Academic Tools** → arXiv papers, summaries, PDFs  
📁 **File Operations** → Write, manage, organize files  


## 🚀 Quick Start

```bash
# 1. Clone & Setup
git clone https://github.com/Sampavi01/Knowledge-MCP.git
cd Knowledge-MCP

# 2. Create Virtual Environment
uv venv

# 3. Activate Virtual Environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 4. Install Dependencies
uv sync

# 5. Configure Environment
echo "GROQ_API_KEY=your_groq_api_key_here" > .env

# 6. Run Chatbot
uv run mcp_chatbot.py
```

## 📂 Project Structure

```
MCP Project/
├── 🚀 mcp_chatbot.py
├── 🔬 mcp_server.py
├── ⚙️ server_config.json
├── 📱 mcp_client.py
├── 📦 pyproject.toml
├── 📚 research_papers/
│   └── 📄 papers.json
├── 📁 papers/
├── 🔒 .env
├── 🐍 .python-version
├── 🔧 uv.lock
└── 📖 README.md
```

## 🧪 Test

```bash
# Test chatbot
uv run mcp_chatbot.py

# Test server
uv run mcp_server.py
```

## 🆘 Need Help?

- 🐛 **Issues**: [GitHub Issues](https://github.com/Sampavi01/Knowledge-MCP/issues)
- 💬 **Questions**: [Discussions](https://github.com/Sampavi01/Knowledge-MCP/discussions)

---

<div align="center">

**⚡ Built with MCP + Groq + Python ⚡**

[⭐ Star](https://github.com/Sampavi01/Knowledge-MCP) • [🔀 Fork](https://github.com/Sampavi01/Knowledge-MCP)

</div>
