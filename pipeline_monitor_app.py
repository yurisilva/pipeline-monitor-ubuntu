#!/usr/bin/env python3
"""
Pipeline Monitor - Main Application

Monitors GitHub Actions pipeline status and displays it in system tray.
Configure via config.json file.
"""

import signal
import sys
from pathlib import Path
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
from gi.repository import Gtk, AppIndicator3, GLib

from pipeline_monitor.tray_icon import TrayIcon
from pipeline_monitor.settings import Settings
from pipeline_monitor.github_client import GitHubClient
from pipeline_monitor.monitor import PipelineMonitor
from pipeline_monitor.settings_dialog import SettingsDialog


class PipelineMonitorApp:
    """Main application that integrates all components."""

    def __init__(self, config_path: str = "config.json") -> None:
        """Initialize the pipeline monitor application."""
        self.config_path = Path(config_path)

        # Load settings
        if self.config_path.exists():
            self.settings = Settings.load(str(self.config_path))
            print(f"Loaded settings from {self.config_path}")
        else:
            print(f"Config file not found: {self.config_path}")
            print("Please create config.json with:")
            print('{')
            print('  "github_repo_url": "owner/repo",')
            print('  "api_token": "your_github_token",')
            print('  "poll_interval_seconds": 120')
            print('}')
            sys.exit(1)

        # Extract owner and repo from URL
        repo_parts = self.settings.github_repo_url.split("/")
        if len(repo_parts) != 2:
            print(f"Invalid repo URL format. Expected 'owner/repo', got: {self.settings.github_repo_url}")
            sys.exit(1)

        repo_owner, repo_name = repo_parts

        # Determine icons directory
        icons_dir = Path(__file__).parent / "icons"

        # Initialize components
        self.tray_icon = TrayIcon(
            icon_name="application-default-icon",
            title="Pipeline Monitor",
            status="running",  # Initial status
            use_custom_icons=icons_dir.exists(),
            icons_dir=str(icons_dir) if icons_dir.exists() else None
        )

        self.github_client = GitHubClient(
            repo_owner=repo_owner,
            repo_name=repo_name,
            api_token=self.settings.api_token
        )

        self.monitor = PipelineMonitor(
            github_client=self.github_client,
            poll_interval=self.settings.poll_interval_seconds
        )

        # Setup AppIndicator
        self.indicator = AppIndicator3.Indicator.new(
            "pipeline-monitor",
            self.tray_icon.icon_name,
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_title(self.tray_icon.title)

        # Create menu
        menu = Gtk.Menu()

        # Status item (disabled, just shows current status)
        self.status_item = Gtk.MenuItem(label="Status: Checking...")
        self.status_item.set_sensitive(False)
        menu.append(self.status_item)

        # Separator
        menu.append(Gtk.SeparatorMenuItem())

        # Check Now item
        item_check_now = Gtk.MenuItem(label="Check Now")
        item_check_now.connect("activate", self.check_now)
        menu.append(item_check_now)

        # Open in GitHub item
        item_open_github = Gtk.MenuItem(label="Open in GitHub")
        item_open_github.connect("activate", self.open_in_github)
        menu.append(item_open_github)

        # Settings item
        item_settings = Gtk.MenuItem(label="Settings...")
        item_settings.connect("activate", self.open_settings)
        menu.append(item_settings)

        # Separator
        menu.append(Gtk.SeparatorMenuItem())

        # Quit item
        item_quit = Gtk.MenuItem(label="Quit")
        item_quit.connect("activate", self.quit)
        menu.append(item_quit)

        menu.show_all()
        self.indicator.set_menu(menu)

        # Register for status changes
        self.monitor.on_status_change(self.on_status_changed)

        # Start polling in background using GLib timeout
        GLib.timeout_add_seconds(
            self.settings.poll_interval_seconds,
            self.poll_status
        )

        # Do initial poll
        self.poll_status()

        print(f"Monitoring: {self.settings.github_repo_url}")
        print(f"Poll interval: {self.settings.poll_interval_seconds}s")
        print("System tray icon should be visible. Right-click and select 'Quit' to exit.")

    def poll_status(self) -> bool:
        """Poll status once. Returns True to continue GLib timeout."""
        self.monitor._poll_once()
        return True  # Continue polling

    def on_status_changed(self, new_status: str) -> None:
        """Handle status change from monitor."""
        print(f"Status changed to: {new_status}")

        # Update tray icon
        self.tray_icon.update_status(new_status)
        self.indicator.set_icon(self.tray_icon.icon_name)

        # Update menu item
        status_text = {
            "passed": "✓ Passed",
            "failed": "✗ Failed",
            "running": "⟳ Running"
        }.get(new_status, new_status)

        self.status_item.set_label(f"Status: {status_text}")

        # Show desktop notification (if enabled)
        if self.settings.enable_notifications:
            self.show_notification(new_status, status_text)

    def show_notification(self, status: str, status_text: str) -> None:
        """Show desktop notification for status change."""
        import subprocess

        title = "Pipeline Monitor"
        icon_map = {
            "passed": "dialog-ok",
            "failed": "dialog-error",
            "running": "dialog-warning"
        }
        icon = icon_map.get(status, "dialog-information")

        message = f"{self.settings.github_repo_url}\n{status_text}"

        # Use notify-send for desktop notifications
        try:
            subprocess.run(
                ["notify-send", "-i", icon, title, message],
                check=False
            )
        except FileNotFoundError:
            print("notify-send not found, skipping notification")

    def check_now(self, _source: Gtk.MenuItem) -> None:
        """Force an immediate poll."""
        print("Checking pipeline status now...")
        self.poll_status()

    def open_in_github(self, _source: Gtk.MenuItem) -> None:
        """Open GitHub Actions page in browser."""
        import webbrowser
        url = f"https://github.com/{self.settings.github_repo_url}/actions"
        print(f"Opening: {url}")
        webbrowser.open(url)

    def open_settings(self, _source: Gtk.MenuItem) -> None:
        """Open settings dialog."""
        dialog = SettingsDialog(None, self.settings)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            # Save new settings
            new_settings = dialog.get_settings()
            new_settings.save(str(self.config_path))
            print("Settings saved! Please restart the application for changes to take effect.")

        dialog.destroy()

    def quit(self, _source: Gtk.MenuItem) -> None:
        """Quit the application."""
        print("Quitting...")
        self.monitor.stop()
        Gtk.main_quit()

    def run(self) -> None:
        """Run the application."""
        # Handle Ctrl+C gracefully
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        Gtk.main()


def main() -> None:
    """Entry point."""
    app = PipelineMonitorApp()
    app.run()


if __name__ == "__main__":
    main()
