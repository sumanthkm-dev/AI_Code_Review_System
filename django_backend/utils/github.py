import requests
import base64
from urllib.parse import urlparse
from uuid import uuid4
from .ai_agent import analyse_code_with_llm


def get_owner_and_repo(url):
    parsed_url = urlparse(url=url)
    path_parts = parsed_url.path.strip("/").split("/")
    if len(path_parts > 2):
        owner, repo = path_parts[0], path_parts[1]
        return path_parts
    return None


def fetch_pr_files(repo_url, pr_number, github_token=None):
    """_summary_
    Build url for to fetch file content.
    """
    owner, repo = get_owner_and_repo(repo_url)
    file_url = f"https://api.github.com/{owner}/{repo}/pulls/{pr_number}/files"
    headers = {"Authorization": f"token { github_token}"} if github_token else {}
    response = requests.get(url=file_url, headers=headers)
    response.raise_for_status()
    return response.json()


def fetch_file_content(repo_url, file_path, github_token=None):
    owner, repo = get_owner_and_repo(repo_url)
    file_url = f"https://api.github.com/{owner}/{repo}/contents/{file_path}"
    headers = {"Authorization": f"token { github_token}"} if github_token else {}
    response = requests.get(url=file_url, headers=headers)
    response.raise_for_status()
    content = response.json()
    return base64.b64decode(content["content"]).decode()


def analyse_pr(repo_url, pr_number, github_token=None):
    task_id = str(uuid4())
    try:
        pr_fies = fetch_pr_files(repo_url, pr_number, github_token)
        analysis_results = []
        for file in pr_fies:
            file_name = file["filename"]
            raw_content = fetch_file_content(repo_url, file_name, github_token)
            analysis_result = analyse_code_with_llm(raw_content, file_name)
            analysis_results.append(
                {"results": analysis_result, "file_name": file_name}
            )
        return {"task_id": task_id, "results": analysis_results}
    except Exception as e:
        print(e)
        return {"task_id": task_id, "results": []}
