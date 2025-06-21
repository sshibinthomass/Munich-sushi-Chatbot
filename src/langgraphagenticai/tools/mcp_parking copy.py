import json
import sys
import requests
from pathlib import Path
from typing import List, Dict
from mcp.server.fastmcp import FastMCP


current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent.parent
sys.path.append(str(project_root))


mcp=FastMCP("Parking near restaurant", port=8003)

@mcp.tool()
def get_parking_data() -> dict:
    """
    Get available parking spaces in Munich.
    Returns:
        dict: The details about the available parking spaces in Munich.
    """
    with open(project_root / "data/parking.json", "r", encoding="utf-8") as f:
        return json.load(f)

if __name__=="__main__":
    mcp.run(transport="streamable-http")
