import wikipedia
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("WikipediaSearch")

@mcp.tool()
def fetch_wikipedia_info(query: str) -> dict:
    """
    Search Wikipedia for a topic and return title, summary, and URL of the best match.
    """
    try:
        search_results = wikipedia.search(query)
        if not search_results:
            return {"error": "No results found for your query."}

        best_match = search_results[0]
        page = wikipedia.page(best_match)

        return {
            "title": page.title,
            "summary": page.summary,
            "url": page.url
        }

    except wikipedia.DisambiguationError as e:
        return {
            "error": f"Ambiguous topic. Try one of these: {', '.join(e.options[:5])}"
        }

    except wikipedia.PageError:
        return {
            "error": "No Wikipedia page could be loaded for this query."
        }
    

@mcp.tool()
def list_wikipedia_sections(topic: str) -> dict:
    """
    List sections of a Wikipedia page for a given topic.
    """
    try:
        page = wikipedia.page(topic)
        return {
            "title": page.title,
            "sections": page.sections
        }

    except wikipedia.PageError:
        return {
            "error": "No Wikipedia page could be loaded for this topic."
        }

    except wikipedia.DisambiguationError as e:
        return {
            "error": f"Ambiguous topic. Try one of these: {', '.join(e.options[:5])}"
        } 

@mcp.tool()
def get_section_content(topic: str, section: str) -> dict:
    """
    Get the content of a specific section from a Wikipedia page.
    """
    try:
        page = wikipedia.page(topic)
        if section not in page.sections:
            return {
                "error": f"Section '{section}' not found in the page '{topic}'."
            }
        
        section_content = page.section(section)
        if section_content is None:
            return {
                "error": f"Section `{section}` is not available in the page `{topic}`."
            }
        return {
            "title": page.title,
            "section": section,
            "content": section_content
        }

    except wikipedia.PageError:
        return {
            "error": "No Wikipedia page could be loaded for this topic."
        }

    except wikipedia.DisambiguationError as e:
        return {
            "error": f"Ambiguous topic. Try one of these: {', '.join(e.options[:5])}"
        }

# Run the MCP server
if __name__ == "__main__":
    print("Starting MCP Wikipedia Server...")
    mcp.run(transport="stdio")
