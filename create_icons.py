#!/usr/bin/env python3
"""Create simple colored circle icons for the pipeline monitor."""

from pathlib import Path

# Create SVG icons
def create_svg_icon(color, filename):
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">
  <circle cx="32" cy="32" r="28" fill="{color}" stroke="#333" stroke-width="2"/>
</svg>'''
    Path(filename).write_text(svg_content)
    print(f"Created: {filename}")

# Create icons directory
icons_dir = Path(__file__).parent / "icons"
icons_dir.mkdir(exist_ok=True)

# Create red, yellow, green icons
create_svg_icon("#dc2626", icons_dir / "pipeline-red.svg")     # Red (failed)
create_svg_icon("#eab308", icons_dir / "pipeline-yellow.svg")  # Yellow (running)
create_svg_icon("#16a34a", icons_dir / "pipeline-green.svg")   # Green (passed)

print("\nIcons created successfully!")
print(f"Location: {icons_dir.absolute()}")
