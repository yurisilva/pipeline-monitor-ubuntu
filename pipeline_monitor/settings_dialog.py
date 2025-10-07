"""Settings dialog GUI for Pipeline Monitor."""

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from pipeline_monitor.settings import Settings


class SettingsDialog(Gtk.Dialog):
    """GTK dialog for editing settings."""

    def __init__(self, parent, current_settings: Settings):
        super().__init__(title="Pipeline Monitor Settings", parent=parent)
        self.current_settings = current_settings

        # Set dialog properties
        self.set_default_size(500, 250)
        self.set_modal(True)

        # Add buttons
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("Save", Gtk.ResponseType.OK)

        # Create content area
        box = self.get_content_area()
        box.set_spacing(10)
        box.set_margin_start(10)
        box.set_margin_end(10)
        box.set_margin_top(10)
        box.set_margin_bottom(10)

        # GitHub Repo URL
        label_repo = Gtk.Label(label="GitHub Repository (owner/repo):")
        label_repo.set_halign(Gtk.Align.START)
        box.pack_start(label_repo, False, False, 0)

        self.entry_repo = Gtk.Entry()
        self.entry_repo.set_text(current_settings.github_repo_url)
        self.entry_repo.set_placeholder_text("e.g., torvalds/linux")
        box.pack_start(self.entry_repo, False, False, 0)

        # API Token
        label_token = Gtk.Label(label="GitHub API Token:")
        label_token.set_halign(Gtk.Align.START)
        box.pack_start(label_token, False, False, 0)

        self.entry_token = Gtk.Entry()
        self.entry_token.set_text(current_settings.api_token)
        self.entry_token.set_placeholder_text("ghp_xxxxxxxxxxxx")
        self.entry_token.set_visibility(False)  # Hide token
        self.entry_token.set_input_purpose(Gtk.InputPurpose.PASSWORD)
        box.pack_start(self.entry_token, False, False, 0)

        # Poll Interval
        label_interval = Gtk.Label(label="Poll Interval (seconds):")
        label_interval.set_halign(Gtk.Align.START)
        box.pack_start(label_interval, False, False, 0)

        self.spin_interval = Gtk.SpinButton()
        adjustment = Gtk.Adjustment(
            value=current_settings.poll_interval_seconds,
            lower=30,
            upper=600,
            step_increment=10,
            page_increment=60
        )
        self.spin_interval.set_adjustment(adjustment)
        box.pack_start(self.spin_interval, False, False, 0)

        # Enable Notifications checkbox
        self.check_notifications = Gtk.CheckButton(label="Enable Desktop Notifications")
        self.check_notifications.set_active(current_settings.enable_notifications)
        box.pack_start(self.check_notifications, False, False, 10)

        self.show_all()

    def get_settings(self) -> Settings:
        """Get settings from dialog fields."""
        return Settings(
            github_repo_url=self.entry_repo.get_text().strip(),
            api_token=self.entry_token.get_text().strip(),
            poll_interval_seconds=int(self.spin_interval.get_value()),
            enable_notifications=self.check_notifications.get_active()
        )
