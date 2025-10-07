# Pipeline Monitor

A system tray application for monitoring GitHub Actions pipeline status on Ubuntu.

## Features

- 🔴 **Red icon** - Pipeline failed
- 🟡 **Yellow icon** - Pipeline running
- 🟢 **Green icon** - Pipeline passed
- Auto-polls GitHub Actions API every 2 minutes (configurable)
- System tray integration for Ubuntu

## Setup

### 1. Install System Dependencies

```bash
sudo apt-get install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-appindicator3-0.1
```

### 2. Install Python Dependencies

```bash
pip install requests
```

### 3. Create Configuration File

Copy the example config and edit it:

```bash
cp config.json.example config.json
```

Edit `config.json` with your GitHub repository details:

```json
{
  "github_repo_url": "your-username/your-repo",
  "api_token": "ghp_your_github_token_here",
  "poll_interval_seconds": 120
}
```

**Getting a GitHub token:**
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` and `workflow` scopes
3. Copy the token to config.json

## Running

```bash
PYTHONPATH=/home/yuri/Workspaces/ai-bootcamp:$PYTHONPATH /usr/bin/python3 pipeline_monitor_app.py
```

Or create a simple wrapper script `run.sh`:

```bash
#!/bin/bash
PYTHONPATH="$(dirname "$0"):$PYTHONPATH" /usr/bin/python3 "$(dirname "$0")/pipeline_monitor_app.py"
```

Make it executable:
```bash
chmod +x run.sh
./run.sh
```

The system tray icon will appear in your top panel. Right-click it and select "Quit" to exit.

## Development

This project was built using Test-Driven Development (TDD) with specialized sub-agents.

### Running Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_tray_icon.py -v
```

### Code Quality

```bash
# Lint and format
ruff check --fix
ruff format

# Type checking
mypy .

# Security scan
bandit -r pipeline_monitor/

# All checks
pytest && ruff check && mypy .
```

## Architecture

Built with clean separation of concerns:

- `TrayIcon` - System tray icon state management
- `Settings` - Configuration persistence (save/load JSON)
- `GitHubClient` - GitHub Actions API client
- `PipelineMonitor` - Polling logic and change detection
- `PipelineMonitorApp` - Main application integration

All components are fully tested with pytest.

## License

MIT
