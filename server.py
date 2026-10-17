import os
import hashlib
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers

# Initialize the FastMCP server
mcp = FastMCP("Exam Challenge MCP Server")

# Your registered exam email
NORMALIZED_EMAIL = "24f2009249@ds.study.iitm.ac.in"

@mcp.tool
def solve_challenge() -> str:
    """
    Exposes the required solve_challenge tool with no required properties in its input schema.
    Reads the challenge dynamically from the incoming HTTP request headers.
    """
    headers = get_http_headers()
    
    # Extract X-Exam-Challenge header (normalized to lowercase by ASGI/Starlette)
    challenge = headers.get("x-exam-challenge", "").strip()
    
    # Format: ${challenge}:${normalizedEmail}
    raw_data = f"{challenge}:{NORMALIZED_EMAIL}"
    
    # Compute SHA-256 hash
    sha256_hash = hashlib.sha256(raw_data.encode("utf-8")).hexdigest()
    
    # Return the first 16 lowercase hex characters
    return sha256_hash[:16]

if __name__ == "__main__":
    # Render assigns a dynamic port; fallback to 8000 for local testing
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="http", host="0.0.0.0", port=port)