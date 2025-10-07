#!/bin/bash
# Pipeline Monitor - Run in background

cd "$(dirname "$0")"
nohup /usr/bin/python3 pipeline_monitor_app.py > pipeline-monitor.log 2>&1 &
echo "Pipeline Monitor started in background (PID: $!)"
echo "Logs: $(pwd)/pipeline-monitor.log"
echo "To stop: kill $!"
