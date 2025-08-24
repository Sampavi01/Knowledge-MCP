import arxiv
import json
import os
from typing import List, Dict
from mcp.server.fastmcp import FastMCP

DATA_DIR = "research_papers"

# Initialize FastMCP server
mcp = FastMCP("academic_assistant")

def _sanitize_topic(topic: str) -> str:
    """Make topic safe for folder names."""
    return topic.strip().lower().replace(" ", "_")

# -------- Tool 1: Fetch Papers -------- #
@mcp.tool()
def fetch_papers(topic: str, limit: int = 5) -> Dict[str, str]:
    """
    Fetch papers from arXiv on a given topic.
    Returns: paper_id -> paper_title
    """
    client = arxiv.Client()
    search_query = arxiv.Search(
        query=topic,
        max_results=limit,
        sort_by=arxiv.SortCriterion.Relevance
    )
    results = client.results(search_query)

    topic_dir = os.path.join(DATA_DIR, _sanitize_topic(topic))
    os.makedirs(topic_dir, exist_ok=True)
    json_file = os.path.join(topic_dir, "papers.json")

    try:
        with open(json_file, "r") as f:
            papers_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        papers_data = {}

    summary = {}
    for paper in results:
        pid = paper.get_short_id()
        summary[pid] = paper.title
        papers_data[pid] = {
            "title": paper.title,
            "authors": [a.name for a in paper.authors],
            "abstract": paper.summary,
            "pdf": paper.pdf_url,
            "published_on": str(paper.published.date())
        }

    with open(json_file, "w") as f:
        json.dump(papers_data, f, indent=2)

    return summary


# -------- Tool 2: Get Paper Details -------- #
@mcp.tool()
def get_paper_details(paper_id: str) -> Dict[str, str]:
    """
    Retrieve details of a paper by ID.
    Returns title, authors, abstract, and PDF link.
    """
    if not os.path.exists(DATA_DIR):
        return {"error": "No papers saved yet."}

    for topic in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, topic, "papers.json")
        if os.path.isfile(path):
            try:
                with open(path, "r") as f:
                    papers_data = json.load(f)
                    if paper_id in papers_data:
                        info = papers_data[paper_id]
                        return {
                            "title": info.get("title", ""),
                            "authors": ", ".join(info.get("authors", [])),
                            "abstract": info.get("abstract", ""),
                            "pdf_link": info.get("pdf", "")
                        }
            except Exception:
                continue

    return {"error": f"No information found for paper {paper_id}."}


# -------- Tool 3: Summarize Topic (Optional but Recommended) -------- #
@mcp.tool()
def summarize_topic(topic: str, limit: int = 5) -> Dict[str, list]:
    """
    Fetch top N papers on a topic and return a short summary for each.
    No local saving required.
    """
    client = arxiv.Client()
    search_query = arxiv.Search(
        query=topic,
        max_results=limit,
        sort_by=arxiv.SortCriterion.Relevance
    )
    results = client.results(search_query)

    summaries = []
    for paper in results:
        abstract = paper.summary or ""
        short_summary = ". ".join(abstract.split(". ")[:3]) + "..."
        summaries.append(f"{paper.title} → {short_summary}")

    return {"summary": summaries}


@mcp.tool()
def write_to_file(filename: str, content: str) -> str:
    """
    Write content to a file.
    
    Args:
        filename: Name of the file to write to
        content: Content to write to the file
        
    Returns:
        Success message or error message
    """
    try:
        # Clean up the content by removing excessive whitespace
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped:  # Only add non-empty lines
                cleaned_lines.append(stripped)
        
        # Join with single newlines and add one final newline
        cleaned_content = '\n'.join(cleaned_lines) + '\n'
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(cleaned_content)
        return f"Successfully wrote cleaned content to {filename}"
    except Exception as e:
        return f"Error writing to file: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="stdio")