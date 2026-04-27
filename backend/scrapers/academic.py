import requests
import xml.etree.ElementTree as ET
from typing import List

def search_arxiv(query: str, max_results: int = 5) -> List[dict]:
    """
    Search ArXiv for recent academic papers.
    """
    base_url = "http://export.arxiv.org/api/query?"
    params = f"search_query=all:{query}&start=0&max_results={max_results}&sortBy=relevance&sortOrder=descending"
    
    try:
        response = requests.get(base_url + params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"ArXiv API error: {e}")
        return []

    try:
        root = ET.fromstring(response.content)
    except ET.ParseError as e:
        print(f"Error parsing ArXiv XML: {e}")
        return []
    papers = []
    
    # ArXiv API uses Atom format
    namespace = {'atom': 'http://www.w3.org/2005/Atom'}
    
    for entry in root.findall('atom:entry', namespace):
        title = entry.find('atom:title', namespace).text.strip()
        summary = entry.find('atom:summary', namespace).text.strip()
        link = entry.find('atom:id', namespace).text.strip()
        
        papers.append({
            "title": title,
            "summary": summary,
            "link": link
        })
        
    return papers
