import streamlit as st
import json
import os
import glob
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="MCP Research Papers Viewer",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .paper-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .paper-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .paper-authors {
        color: #666;
        font-style: italic;
        margin-bottom: 0.5rem;
    }
    .paper-abstract {
        color: #333;
        line-height: 1.5;
        margin-bottom: 1rem;
    }
    .paper-links {
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
    }
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def load_papers_data():
    papers_data = {}
    research_dir = Path("research_papers")
    if not research_dir.exists():
        return papers_data
    json_files = glob.glob(str(research_dir / "**" / "papers.json"), recursive=True)
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                topic_data = json.load(f)
                topic_name = Path(json_file).parent.name
                papers_data[topic_name] = topic_data
        except Exception as e:
            st.error(f"Error loading {json_file}: {e}")
    return papers_data

def display_paper_card(paper_id, paper_info):
    with st.container():
        st.markdown(f"""
        <div class="paper-card">
            <div class="paper-title">{paper_info.get('title', 'No title')}</div>
            <div class="paper-authors">Authors: {', '.join(paper_info.get('authors', ['Unknown']))}</div>
            <div class="paper-abstract">{paper_info.get('abstract', 'No abstract available')}</div>
            <div class="paper-links">
                <strong>Published:</strong> {paper_info.get('published_on', 'Unknown')}
                <strong>ID:</strong> {paper_id}
            </div>
        </div>
        """, unsafe_allow_html=True)
        if paper_info.get('pdf'):
            st.link_button("📄 View PDF", paper_info['pdf'], type="primary")
        paper_json = json.dumps(paper_info, indent=2)
        st.download_button(
            label="💾 Download Paper Info",
            data=paper_json,
            file_name=f"{paper_id}_paper_info.json",
            mime="application/json"
        )

def main():
    st.markdown('<h1 class="main-header">🔬 MCP Research Papers Viewer</h1>', unsafe_allow_html=True)

    papers_data = load_papers_data()
    if not papers_data:
        st.warning("No research papers found. Use the MCP chatbot to fetch some papers first!")
        st.info("Try running: `uv run mcp_chatbot.py` and ask for papers on a topic.")
        return

    # Statistics cards
    total_topics = len(papers_data)
    total_papers = sum(len(papers) for papers in papers_data.values())
    col1, col2, col3 = st.columns(3)
    col1.markdown(f"""
        <div class="stats-card">
            <h3>📚 Total Topics</h3>
            <h2>{total_topics}</h2>
        </div>
    """, unsafe_allow_html=True)
    col2.markdown(f"""
        <div class="stats-card">
            <h3>📄 Total Papers</h3>
            <h2>{total_papers}</h2>
        </div>
    """, unsafe_allow_html=True)
    col3.markdown(f"""
        <div class="stats-card">
            <h3>🔍 Research Areas</h3>
            <h2>{', '.join(papers_data.keys())}</h2>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📖 Browse Papers by Topic")

    selected_topic = st.selectbox(
        "Choose a research topic:",
        options=list(papers_data.keys()),
        format_func=lambda x: x.replace('_', ' ').title()
    )

    if selected_topic:
        topic_papers = papers_data[selected_topic]
        st.markdown(f"### 📋 Papers in **{selected_topic.replace('_', ' ').title()}** ({len(topic_papers)} papers)")

        search_term = st.text_input("🔍 Search papers within this topic:", placeholder="Enter keywords...")
        filtered_papers = topic_papers
        if search_term:
            filtered_papers = {
                pid: info for pid, info in topic_papers.items()
                if search_term.lower() in info.get('title', '').lower() or 
                   search_term.lower() in info.get('abstract', '').lower()
            }
            st.info(f"Found {len(filtered_papers)} papers matching '{search_term}'")

        if filtered_papers:
            for paper_id, paper_info in filtered_papers.items():
                display_paper_card(paper_id, paper_info)
        else:
            st.info("No papers found matching your search criteria.")

if __name__ == "__main__":
    main()
