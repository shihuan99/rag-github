

import os
from typing import List

import requests
from llama_index.core import Document

import env

import urllib3
urllib3.disable_warnings()

def load_documents_from_dir(repo: str,
                            repo_path: str = "",
                            branch: str = "main",
                            extensions: List[str] = None,
                            token: str = None) -> List[Document]:
    """
    从 GitHub 仓库递归读取文件并返回 Document 列表。
    参数:
      - repo: "owner/repo"（例如 "shihuan99/shihuan99.github.io"）
      - repo_path: 仓库内的子路径（例如 "docs/kafka"），为空时扫描整个仓库
      - branch: 分支或提交 SHA（默认 "main"）
      - extensions: 允许的文件扩展名列表（默认 [".md", ".txt"]）
      - token: 可选的 GitHub token（若为 None 则从环境变量 GITHUB_TOKEN 读取）
    返回值:
      - langchain.schema.Document 列表，metadata 中包含 "source"（raw URL）和 "path"
    """
    if extensions is None:
        extensions = [".md", ".txt"]

    owner_repo = (repo or "").strip()
    if not owner_repo or "/" not in owner_repo:
        return []

    if token is None:
        token = os.getenv("GITHUB_TOKEN")

    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    api_url = f"https://api.github.com/repos/{owner_repo}/git/trees/{branch}?recursive=1"
    print('Start loading documents from GitHub repo:', api_url)
    try:
        resp = requests.get(api_url, headers=headers, timeout=15, proxies=env.proxies, verify=False)
        if resp.status_code != 200:
            return []
        tree = resp.json().get("tree", [])
    except Exception:
        return []

    docs: List[Document] = []
    repo_path_norm = repo_path.strip().rstrip("/")

    for item in tree:
        if item.get("type") != "blob":
            continue
        path = item.get("path", "")
        if repo_path_norm:
            if not (path == repo_path_norm or path.startswith(repo_path_norm + "/")):
                continue
        if not any(path.lower().endswith(ext) for ext in extensions):
            continue
        raw_url = f"https://raw.githubusercontent.com/{owner_repo}/{branch}/{path}"
        try:
            r = requests.get(raw_url, headers=headers, timeout=15, proxies=env.proxies, verify=False)
            if r.status_code != 200:
                continue
            text = r.text
        except Exception:
            continue
        docs.append(Document(text=text, metadata={"source": raw_url, "path": path}))
        print(path)
    print(f"Loaded {len(docs)} documents from GitHub repository.")
    return docs

documents = load_documents_from_dir(
    repo=os.environ['GITHUB_URL'],
    repo_path=os.environ['GITHUB_START_PATH'],
    branch=os.environ['GITHUB_BRANCH'],
    extensions=[".md", ".txt"]
)