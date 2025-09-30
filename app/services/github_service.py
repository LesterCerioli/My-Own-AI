import requests
import base64
from app.config import settings
from app.schemas import GitHubCredentials, FileStructure
import logging

logger = logging.getLogger(__name__)

class GitHubService:
    def __init__(self):
        self.api_url = settings.GITHUB_API_URL

    def create_repository(self, credentials: GitHubCredentials) -> str:
        url = f"{self.api_url}/user/repos"
        data = {
            "name": credentials.repo_name,
            "description": "AI-generated project",
            "private": False,
            "auto_init": False
        }
        
        response = requests.post(
            url,
            json=data,
            auth=(credentials.username, credentials.password)
        )
        response.raise_for_status()
        
        repo_data = response.json()
        return repo_data["html_url"]

    def create_branch(self, credentials: GitHubCredentials, repo_name: str, branch: str = "smartai"):
        
        url = f"{self.api_url}/repos/{credentials.username}/{repo_name}/git/refs/heads/main"
        response = requests.get(url, auth=(credentials.username, credentials.password))
        
        if response.status_code == 404:
            
            url = f"{self.api_url}/repos/{credentials.username}/{repo_name}/git/refs/heads/master"
            response = requests.get(url, auth=(credentials.username, credentials.password))
        
        response.raise_for_status()
        main_sha = response.json()["object"]["sha"]
                
        url = f"{self.api_url}/repos/{credentials.username}/{repo_name}/git/refs"
        data = {
            "ref": f"refs/heads/{branch}",
            "sha": main_sha
        }
        
        response = requests.post(url, json=data, auth=(credentials.username, credentials.password))
        response.raise_for_status()

    def commit_files(self, credentials: GitHubCredentials, repo_name: str, files: list, branch: str = "smartai"):
        for file in files:
            self._create_file(credentials, repo_name, file["path"], file["content"], branch)

    def _create_file(self, credentials: GitHubCredentials, repo_name: str, path: str, content: str, branch: str):
        url = f"{self.api_url}/repos/{credentials.username}/{repo_name}/contents/{path}"
        
        data = {
            "message": f"Add {path}",
            "content": base64.b64encode(content.encode()).decode(),
            "branch": branch
        }
        
        response = requests.put(url, json=data, auth=(credentials.username, credentials.password))
        response.raise_for_status()