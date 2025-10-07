#!/bin/bash
# Pipeline Monitor - Simple run script

cd "$(dirname "$0")"
PYTHONPATH="$PWD:$PYTHONPATH" /usr/bin/python3 pipeline_monitor_app.py
