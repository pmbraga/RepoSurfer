# mcp_server.py
import argparse
import os
from typing import List
from mcp.server.fastmcp import FastMCP

from github import Github

with open("REPO_NAME.txt", "r") as f:
    repo_name = f.readline().strip()
with open("GITHUB_TOKEN.txt", "r") as f:
    auth_token = f.readline().strip()

# Authentication is defined via github.Auth
from github import Auth
auth = Auth.Token(auth_token)
# Public Web Github
g = Github(auth=auth)
g.get_user().login

# repo_name = "TEST_USER/TEST_REPO"

# Initialize the MCP server
mcp = FastMCP("FilesystemServer")

@mcp.tool()
def get_repo_branches() -> List[str]:
    """
    Get a list of all branches for a specific repository.
    """
    repo = g.get_repo(f'{repo_name}')

    # Fetch branches
    all_items = repo.get_branches()

    return [i.name for i in all_items]

@mcp.tool()
def get_repo_pulls(state) -> List[str]:
    """
    Get a list of pull requests for a specific repository. State can be open or closed.
    """
    repo = g.get_repo(f'{repo_name}')

    # Fetch pull requests
    pulls = repo.get_pulls(state=state)
    return [f"#{pr.number} {pr.title}  —  by {pr.user.login}  [{pr.state}]" for pr in pulls]

@mcp.tool()
def get_repo_issues(state) -> List[str]:
    """
    Get a list of issues for a specific repository. State can be open or closed.
    """
    repo = g.get_repo(f'{repo_name}')

    # Fetch issues
    issues = repo.get_issues(state=state)
    return [f"#{i.number} {i.title}  —  by {i.user.login}  [{i.state}]" for i in issues]

@mcp.tool()
def get_repo_comments(issue_number: int) -> List[str]:
    """
    Get comments for a specific issue in a repository.
    """
    repo = g.get_repo(f'{repo_name}')
    issue = repo.get_issue(number=issue_number)
    comments = issue.get_comments()
    return [f"{comment.user.login}: {comment.body}" for comment in comments]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MCP Filesystem Server")
    parser.add_argument(
        "transport",
        choices=["stdio", "sse"],
        help="Transport mode (stdio or sse)",
    )
    args = parser.parse_args()

    # Start the MCP server
    mcp.run(transport=args.transport)



