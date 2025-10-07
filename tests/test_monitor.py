import pytest
from unittest.mock import Mock, patch, call
from pipeline_monitor.monitor import PipelineMonitor


def test_monitor_calls_callback_when_status_changes_from_running_to_passed():
    """Test that PipelineMonitor calls the callback when pipeline status changes from 'running' to 'passed'."""
    # Arrange
    mock_github_client = Mock()
    # First poll: status is "running", second poll: status is "passed"
    mock_github_client.get_pipeline_status.side_effect = ["running", "passed"]

    callback = Mock()
    monitor = PipelineMonitor(
        github_client=mock_github_client,
        poll_interval=0.1  # Use short interval for testing (100ms)
    )

    # Register the callback to be notified of status changes
    monitor.on_status_change(callback)

    # Act
    with patch("time.sleep") as mock_sleep:
        # Start monitoring in a controlled way
        monitor.start()

        # Simulate two poll cycles
        # First cycle: get "running" status
        monitor._poll_once()

        # Second cycle: get "passed" status
        monitor._poll_once()

        monitor.stop()

    # Assert
    # Callback should be called once when status changes from "running" to "passed"
    callback.assert_called_once_with("passed")

    # Verify GitHub client was polled twice
    assert mock_github_client.get_pipeline_status.call_count == 2
