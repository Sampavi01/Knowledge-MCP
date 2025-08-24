import arxiv
import json
import os
from typing import List, Dict
from mcp.server.fastmcp import FastMCP

DATA_DIR = "research_papers"

# Initialize FastMCP server
mcp = FastMCP("academic_assistant")

@mcp.tool()
def fetch_papers(topic: str, limit: int = 5) -> Dict[str, str]:
    """
    Fetch papers from Arxiv on a given topic.
    Returns a dictionary: paper_id -> paper_title
    """
    client = arxiv.Client()
    search_query = arxiv.Search(
        query=topic,
        max_results=limit,
        sort_by=arxiv.SortCriterion.Relevance
    )
    results = client.results(search_query)

    topic_dir = os.path.join(DATA_DIR, topic.lower().replace(" ", "_"))
    os.makedirs(topic_dir, exist_ok=True)
    json_file = os.path.join(topic_dir, "papers.json")

    try:
        with open(json_file, "r") as f:
            papers_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        papers_data = {}

    paper_summary = {}
    for paper in results:
        pid = paper.get_short_id()
        paper_summary[pid] = paper.title
        papers_data[pid] = {
            "title": paper.title,
            "authors": [a.name for a in paper.authors],
            "abstract": paper.summary,
            "pdf": paper.pdf_url,
            "published_on": str(paper.published.date())
        }

    with open(json_file, "w") as f:
        json.dump(papers_data, f, indent=2)

    return paper_summary

@mcp.tool()
def get_paper_details(paper_id: str) -> Dict[str, str]:
    """
    Retrieve essential details of a paper by ID.
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

@mcp.tool()
def compute_math(expression: str) -> str:
    """
    Safely compute a simple math expression.
    Example: '2 + 3 * 4'
    """
    try:
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
