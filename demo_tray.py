#!/usr/bin/env python3
"""Quick demo script to see the system tray icon in action."""

import signal
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
from gi.repository import Gtk, AppIndicator3

from pipeline_monitor.tray_icon import TrayIcon


def main() -> None:
    """Run the system tray demo."""
    # Create our TrayIcon with different statuses
    # Try changing status to "running" or "passed" to see different Ubuntu system icons:
    # - "failed" shows dialog-error (red X)
    # - "running" shows dialog-warning (yellow warning triangle)
    # - "passed" shows dialog-ok (green checkmark)
    tray = TrayIcon(icon_name="application-default-icon", title="Pipeline Monitor", status="running")

    print(f"Creating tray icon with: {tray.icon_name}")

    # Create AppIndicator
    indicator = AppIndicator3.Indicator.new(
        "pipeline-monitor",
        tray.icon_name,  # Use our status-based icon name
        AppIndicator3.IndicatorCategory.APPLICATION_STATUS
    )
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    indicator.set_title(tray.title)

    # Create a simple menu (required by AppIndicator)
    menu = Gtk.Menu()

    # Add a quit menu item
    item_quit = Gtk.MenuItem(label="Quit")
    item_quit.connect("activate", lambda _: Gtk.main_quit())
    menu.append(item_quit)

    menu.show_all()
    indicator.set_menu(menu)

    print("System tray icon should now be visible!")
    print("Right-click the icon and select 'Quit' to exit.")
    print("\nNote: The icon name is:", tray.icon_name)
    print("This is a real Ubuntu system icon from the freedesktop.org icon theme.")

    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    Gtk.main()


if __name__ == "__main__":
    main()
