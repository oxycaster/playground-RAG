from fastmcp import FastMCP
from search_vector_store import search_vector_store

mcp = FastMCP("歯科医師国家資格の過去問データベース")

@mcp.tool()
def search(query_text: str, n_results: int = 10) -> list:
    """歯科医師国家試験の過去問データベースで検索を行う"""
    return search_vector_store(query_text, n_results=n_results)

if __name__ == '__main__':
    mcp.run(transport="stdio")