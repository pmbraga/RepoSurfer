# mcp_server.py
import argparse
import os
from pathlib import Path
from typing import List
from mcp.server.fastmcp import FastMCP

from github import Github

# Authentication is defined via github.Auth
from github import Auth

# using an access token
auth = Auth.Token("ENTER YOUR TOKEN")

# Public Web Github
g = Github(auth=auth)
g.get_user().login

# Initialize the MCP server
mcp = FastMCP("FilesystemServer")

# @mcp.tool()
# def get_git_repos() -> List[str]:
#     """
#     Get a list of all repositories for the authenticated user.
#     """
#     repos = g.get_user().get_repos()
#     return [repo.name for repo in repos]

@mcp.tool()
def get_repo_issues(repo_name: str) -> List[str]:
    """
    Get a list of all issues (including PRs) for a specific repository.
    """
    repo = g.get_repo(f'{repo_name}')

    # Fetch issues (this also returns PRs)
    all_items = repo.get_issues()

    return [i.title for i in all_items]

@mcp.tool()
def get_repo_branches(repo_name: str) -> List[str]:
    """
    Get a list of all branches for a specific repository.
    """
    repo = g.get_repo(f'{repo_name}')

    # Fetch branches
    all_items = repo.get_branches()

    return [i.name for i in all_items]

@mcp.tool()
def get_repo_pulls(repo_name: str, state) -> List[str]:
    """
    Get a list of pull requests for a specific repository. State can be open or closed.
    """
    repo = g.get_repo(f'{repo_name}')

    # Fetch pull requests
    pulls = repo.get_pulls(state=state)
    return [f"#{pr.number} {pr.title}  —  by {pr.user.login}  [{pr.state}]" for pr in pulls]

@mcp.tool()
def get_repo_issues(repo_name: str, state) -> List[str]:
    """
    Get a list of issues for a specific repository. State can be open or closed.
    """
    repo = g.get_repo(f'{repo_name}')

    # Fetch issues
    issues = repo.get_issues(state=state)
    return [f"#{i.number} {i.title}  —  by {i.user.login}  [{i.state}]" for i in issues]

@mcp.tool()
def get_repo_comments(repo_name: str, issue_number: int) -> List[str]:
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



