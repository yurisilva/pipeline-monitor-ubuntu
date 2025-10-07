import pytest
from unittest.mock import Mock, patch
from pipeline_monitor.github_client import GitHubClient


def test_get_pipeline_status_returns_passed_when_workflow_succeeds():
    """Test that get_pipeline_status returns 'passed' when GitHub Actions workflow concludes with success."""
    # Arrange
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "workflow_runs": [
            {
                "id": 123456789,
                "status": "completed",
                "conclusion": "success",
                "head_branch": "main"
            }
        ]
    }

    client = GitHubClient(
        repo_owner="example",
        repo_name="repo",
        api_token="ghp_test1234567890"
    )

    # Act
    with patch("requests.get", return_value=mock_response) as mock_get:
        status = client.get_pipeline_status()

    # Assert
    assert status == "passed", "Should return 'passed' when workflow conclusion is 'success'"
    mock_get.assert_called_once()

    # Verify the API was called with correct parameters
    call_args = mock_get.call_args
    assert "https://api.github.com/repos/example/repo/actions/runs" in call_args[0][0]


def test_get_pipeline_status_returns_failed_when_workflow_fails():
    """Test that get_pipeline_status returns 'failed' when GitHub Actions workflow concludes with failure."""
    # Arrange
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "workflow_runs": [
            {
                "id": 987654321,
                "status": "completed",
                "conclusion": "failure",
                "head_branch": "main"
            }
        ]
    }

    client = GitHubClient(
        repo_owner="example",
        repo_name="repo",
        api_token="ghp_test1234567890"
    )

    # Act
    with patch("requests.get", return_value=mock_response) as mock_get:
        status = client.get_pipeline_status()

    # Assert
    assert status == "failed", "Should return 'failed' when workflow conclusion is 'failure'"
    mock_get.assert_called_once()


def test_get_pipeline_status_returns_running_when_workflow_is_in_progress():
    """Test that get_pipeline_status returns 'running' when GitHub Actions workflow is still in progress."""
    # Arrange
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "workflow_runs": [
            {
                "id": 555555555,
                "status": "in_progress",
                "conclusion": None,
                "head_branch": "main"
            }
        ]
    }

    client = GitHubClient(
        repo_owner="example",
        repo_name="repo",
        api_token="ghp_test1234567890"
    )

    # Act
    with patch("requests.get", return_value=mock_response) as mock_get:
        status = client.get_pipeline_status()

    # Assert
    assert status == "running", "Should return 'running' when workflow is in progress with null conclusion"
    mock_get.assert_called_once()
