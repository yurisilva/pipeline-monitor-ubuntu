"""Tests for system tray icon initialization."""

import pytest


def test_tray_icon_initializes_when_created_then_returns_instance():
    """Test that a system tray icon can be initialized.

    This test verifies the most basic behavior: creating a TrayIcon instance
    with required parameters (icon name and title) should succeed and return
    a valid object.
    """
    # Arrange
    icon_name = "application-default-icon"
    title = "Pipeline Monitor"

    # Act
    from pipeline_monitor.tray_icon import TrayIcon

    tray_icon = TrayIcon(icon_name=icon_name, title=title)

    # Assert
    assert tray_icon is not None
    assert isinstance(tray_icon, TrayIcon)


def test_tray_icon_displays_red_icon_when_status_is_failed():
    """Test that tray icon shows red indicator for failed pipeline status.

    This test verifies that when a TrayIcon is created with status="failed",
    it uses a red icon to visually indicate the failure state. For AppIndicator3
    on Ubuntu, this means the icon_name should be set to "dialog-error".

    Expected behavior:
    - Creating TrayIcon with status="failed" should set icon_name to "dialog-error"
    - This provides visual feedback that pipeline has failed

    This test will FAIL because:
    - TrayIcon.__init__() doesn't accept a status parameter yet
    - No logic exists to map status to icon colors
    """
    # Arrange
    from pipeline_monitor.tray_icon import TrayIcon

    title = "Pipeline Monitor"
    status = "failed"

    # Act
    tray_icon = TrayIcon(icon_name="pipeline-monitor", title=title, status=status)

    # Assert
    assert tray_icon.icon_name == "dialog-error", (
        f"Expected icon_name to be 'dialog-error' for failed status, "
        f"but got: {tray_icon.icon_name}"
    )


def test_tray_icon_displays_yellow_icon_when_status_is_running():
    """Test that tray icon shows yellow indicator for running pipeline status.

    This test verifies that when a TrayIcon is created with status="running",
    it uses a yellow icon to visually indicate the running state. For AppIndicator3
    on Ubuntu, this means the icon_name should be set to "dialog-warning".

    Expected behavior:
    - Creating TrayIcon with status="running" should set icon_name to "dialog-warning"
    - This provides visual feedback that pipeline is currently running

    This test will FAIL because:
    - TrayIcon.__init__() doesn't handle status="running" yet
    - No logic exists to map "running" status to yellow icon
    """
    # Arrange
    from pipeline_monitor.tray_icon import TrayIcon

    title = "Pipeline Monitor"
    status = "running"

    # Act
    tray_icon = TrayIcon(icon_name="pipeline-monitor", title=title, status=status)

    # Assert
    assert tray_icon.icon_name == "dialog-warning", (
        f"Expected icon_name to be 'dialog-warning' for running status, "
        f"but got: {tray_icon.icon_name}"
    )


def test_tray_icon_displays_green_icon_when_status_is_passed():
    """Test that tray icon shows green indicator for passed pipeline status.

    This test verifies that when a TrayIcon is created with status="passed",
    it uses a green icon to visually indicate the success state. For AppIndicator3
    on Ubuntu, this means the icon_name should be set to "dialog-ok".

    Expected behavior:
    - Creating TrayIcon with status="passed" should set icon_name to "dialog-ok"
    - This provides visual feedback that pipeline has passed successfully

    This test will FAIL because:
    - TrayIcon.__init__() doesn't handle status="passed" yet
    - No logic exists to map "passed" status to green icon
    """
    # Arrange
    from pipeline_monitor.tray_icon import TrayIcon

    title = "Pipeline Monitor"
    status = "passed"

    # Act
    tray_icon = TrayIcon(icon_name="pipeline-monitor", title=title, status=status)

    # Assert
    assert tray_icon.icon_name == "dialog-ok", (
        f"Expected icon_name to be 'dialog-ok' for passed status, "
        f"but got: {tray_icon.icon_name}"
    )


def test_tray_icon_updates_icon_when_status_changes_from_running_to_passed():
    """Test that tray icon updates its visual indicator when pipeline status changes.

    This test verifies that after a TrayIcon is created with an initial status,
    we can update the status dynamically (e.g., when a running pipeline completes).
    The icon should change from yellow (running) to green (passed) to reflect the
    new state.

    Real-world scenario:
    - Pipeline starts running -> tray icon shows yellow
    - Pipeline completes successfully -> tray icon updates to green
    - User sees real-time status updates in system tray

    Expected behavior:
    - Create TrayIcon with status="running" (icon_name should be "dialog-warning")
    - Call update_status("passed")
    - Icon_name should update to "dialog-ok"

    This test will FAIL because:
    - TrayIcon class doesn't have an update_status() method yet
    - No mechanism exists to change the icon after initialization
    """
    # Arrange
    from pipeline_monitor.tray_icon import TrayIcon

    title = "Pipeline Monitor"
    tray_icon = TrayIcon(icon_name="pipeline-monitor", title=title, status="running")

    # Verify initial state
    assert tray_icon.icon_name == "dialog-warning", (
        "Initial icon should be 'dialog-warning' for running status"
    )

    # Act
    tray_icon.update_status("passed")

    # Assert
    assert tray_icon.icon_name == "dialog-ok", (
        f"Expected icon_name to change to 'dialog-ok' after updating status to 'passed', "
        f"but got: {tray_icon.icon_name}"
    )
