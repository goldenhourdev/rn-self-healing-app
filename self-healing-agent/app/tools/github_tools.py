import os, requests, base64
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}

@tool
def read_file(repo: str, path: str):
    """Reads a file from GitHub."""
    url = f"https://github.com{repo}/contents/{path}"
    r = requests.get(url, headers=headers).json()
    return base64.b64decode(r['content']).decode()

@tool
def write_file(repo: str, path: str, content: str):
    """Writes a fix to GitHub."""
    url = f"https://github.com{repo}/contents/{path}"
    curr = requests.get(url, headers=headers).json()
    payload = {
        "message": "AI Fix",
        "content": base64.b64encode(content.encode()).decode(),
        "sha": curr['sha']
    }
    requests.put(url, headers=headers, json=payload)
    return "Fix applied successfully."

github_tools = [read_file, write_file]
