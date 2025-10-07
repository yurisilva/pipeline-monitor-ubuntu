"""System tray icon module."""

from pathlib import Path


class TrayIcon:
    """Minimal TrayIcon class."""

    def __init__(self, icon_name, title, status=None, use_custom_icons=False, icons_dir=None):
        """Initialize TrayIcon with icon_name and title."""
        self.use_custom_icons = use_custom_icons
        self.icons_dir = Path(icons_dir) if icons_dir else None
        self.title = title

        if status:
            self._set_icon_for_status(status)
        else:
            self.icon_name = icon_name

    def _set_icon_for_status(self, status):
        """Set icon based on status."""
        if self.use_custom_icons and self.icons_dir:
            # Use custom SVG icons
            icon_map = {
                "failed": str(self.icons_dir / "pipeline-red.svg"),
                "running": str(self.icons_dir / "pipeline-yellow.svg"),
                "passed": str(self.icons_dir / "pipeline-green.svg")
            }
            self.icon_name = icon_map.get(status, "application-default-icon")
        else:
            # Use system theme icons
            icon_map = {
                "failed": "dialog-error",
                "running": "dialog-warning",
                "passed": "dialog-ok"
            }
            self.icon_name = icon_map.get(status, "application-default-icon")

    def update_status(self, status):
        """Update icon based on status."""
        self._set_icon_for_status(status)
