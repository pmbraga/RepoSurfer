import argparse
from pathlib import Path
import os
import glob
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("McpServer")

ROOT_DIR = Path(__file__).parent.resolve()


@mcp.tool()
def list_json_files(relative_path: str = "."):
    """
    List files and directories under ROOT_DIR/relative_path. Pass empty string to list root.
    """
    path = (ROOT_DIR / relative_path).resolve()
    if not str(path).startswith(str(ROOT_DIR)):
        return [f"Access denied: {relative_path}"]
    if not path.exists() or not path.is_dir():
        return [f"Not a directory: {relative_path}"]
    return glob.glob(str(path / "*.json"))


@mcp.tool()
def read_codebase(path_to_codebase):
    """
    Load the codebase from the specified path.
    """
    path = (ROOT_DIR / path_to_codebase).resolve()
    if not str(path).startswith(str(ROOT_DIR)):
        return [f"Access denied: {path_to_codebase}"]
    if not path.exists() or not path.is_dir():
        return [f"Not a directory: {path_to_codebase}"]
    files = glob.glob(str(path / "**/*.py"))
    codes = ""
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            code = f.read()
        codes += f"\n\n# File: {file}\n{code}"
    return codes


@mcp.tool()
def read_json(json_file):
    """
    Read a JSON file and return its content.
    """
    import json

    with open(json_file, "r") as file:
        data = json.load(file)
    return data


@mcp.tool()
def save_response(response):
    """
    Save the response to a file.
    """
    with open("response.txt", "w") as file:
        file.write(response)
    return "Response saved to response.txt"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MCP Server")
    parser.add_argument(
        "transport", choices=["stdio", "sse"], help="Transport mode (stdio or sse)"
    )
    args = parser.parse_args()

    mcp.run(transport=args.transport)
