import json


class Settings:
    def __init__(self, github_repo_url, api_token, poll_interval_seconds, enable_notifications=True):
        self.github_repo_url = github_repo_url
        self.api_token = api_token
        self.poll_interval_seconds = poll_interval_seconds
        self.enable_notifications = enable_notifications

    def save(self, file_path):
        data = {
            "github_repo_url": self.github_repo_url,
            "api_token": self.api_token,
            "poll_interval_seconds": self.poll_interval_seconds,
            "enable_notifications": self.enable_notifications
        }
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        # Backward compatibility - default to True if not present
        if "enable_notifications" not in data:
            data["enable_notifications"] = True
        return cls(**data)
