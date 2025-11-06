from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

mcp = FastMCP(name="FastMCP Search")



if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)