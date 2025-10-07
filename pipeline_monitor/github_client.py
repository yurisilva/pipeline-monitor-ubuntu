import requests


class GitHubClient:
    def __init__(self, repo_owner, repo_name, api_token):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.api_token = api_token

    def get_pipeline_status(self):
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/actions/runs"
        headers = {"Authorization": f"Bearer {self.api_token}"}
        response = requests.get(url, headers=headers)
        data = response.json()

        # Check if there are any workflow runs
        if not data.get("workflow_runs"):
            return "running"  # Default to running if no workflows exist

        conclusion = data["workflow_runs"][0]["conclusion"]
        if conclusion is None:
            return "running"
        elif conclusion == "success":
            return "passed"
        elif conclusion == "failure":
            return "failed"
