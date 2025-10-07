import json
import pytest
from pipeline_monitor.settings import Settings


def test_save_settings_to_json_file(tmp_path):
    """Test that Settings can save configuration to a JSON file."""
    # Arrange
    config_file = tmp_path / "config.json"
    settings = Settings(
        github_repo_url="https://github.com/example/repo",
        api_token="ghp_test1234567890",
        poll_interval_seconds=300
    )

    # Act
    settings.save(config_file)

    # Assert
    assert config_file.exists(), "Config file should be created"

    with open(config_file, 'r') as f:
        saved_data = json.load(f)

    assert saved_data["github_repo_url"] == "https://github.com/example/repo"
    assert saved_data["api_token"] == "ghp_test1234567890"
    assert saved_data["poll_interval_seconds"] == 300


def test_load_settings_from_json_file(tmp_path):
    """Test that Settings can load configuration from a JSON file."""
    # Arrange
    config_file = tmp_path / "config.json"

    # Create a settings file first by saving
    original_settings = Settings(
        github_repo_url="https://github.com/test/project",
        api_token="ghp_secret9876543210",
        poll_interval_seconds=600
    )
    original_settings.save(config_file)

    # Act
    loaded_settings = Settings.load(config_file)

    # Assert
    assert loaded_settings.github_repo_url == "https://github.com/test/project"
    assert loaded_settings.api_token == "ghp_secret9876543210"
    assert loaded_settings.poll_interval_seconds == 600
