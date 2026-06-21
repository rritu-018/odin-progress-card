#!/usr/bin/env python3
"""
generate_card.py

Reads progress.json and renders a dark-themed SVG progress card for
The Odin Project, styled similarly to a boot.dev GitHub profile card.

Usage:
    python3 generate_card.py

Input:  progress.json   (hand-edited by you)
Output: odin_progress_card.svg
"""

import json
import datetime
import os

INPUT_FILE = "progress.json"
OUTPUT_FILE = "odin_progress_card.svg"

# ---- Card dimensions & theme (dark, boot.dev-inspired) ----
WIDTH = 500
HEIGHT = 200
BG_COLOR = "#0d1117"
BORDER_COLOR = "#30363d"
ACCENT_COLOR = "#f0a500"      # Odin-ish amber/gold accent
TRACK_COLOR = "#21262d"
TEXT_PRIMARY = "#e6edf3"
TEXT_SECONDARY = "#8b949e"
TITLE_COLOR = "#ffffff"


def load_progress(path):
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Could not find {path}. Create it with course/percent_complete/"
            "current_lesson/projects_completed/projects_total/last_updated."
        )
    with open(path, "r") as f:
        return json.load(f)


def escape_xml(text):
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def format_date(date_str):
    try:
        d = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return d.strftime("%b %d, %Y")
    except (ValueError, TypeError):
        return escape_xml(date_str)


def build_svg(data):
    course = escape_xml(data.get("course", "The Odin Project"))
    percent = data.get("percent_complete", 0)
    percent = max(0, min(100, percent))  # clamp 0-100
    lesson = escape_xml(data.get("current_lesson", "—"))
    proj_done = data.get("projects_completed", 0)
    proj_total = data.get("projects_total", 0)
    last_updated = format_date(data.get("last_updated", ""))

    # Progress bar geometry
    bar_x = 30
    bar_y = 96
    bar_w = WIDTH - 60
    bar_h = 14
    fill_w = round(bar_w * (percent / 100))

    svg = f'''<svg width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The Odin Project progress card">
  <defs>
    <linearGradient id="barGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{ACCENT_COLOR}"/>
      <stop offset="100%" stop-color="#ff6b6b"/>
    </linearGradient>
    <style>
      .title {{ font: 700 20px 'Segoe UI', Helvetica, Arial, sans-serif; fill: {TITLE_COLOR}; }}
      .label {{ font: 600 13px 'Segoe UI', Helvetica, Arial, sans-serif; fill: {TEXT_SECONDARY}; }}
      .value {{ font: 600 13px 'Segoe UI', Helvetica, Arial, sans-serif; fill: {TEXT_PRIMARY}; }}
      .pct {{ font: 700 13px 'Segoe UI', Helvetica, Arial, sans-serif; fill: {TEXT_PRIMARY}; }}
      .footer {{ font: 400 11px 'Segoe UI', Helvetica, Arial, sans-serif; fill: {TEXT_SECONDARY}; }}
      .logo {{ font: 700 13px 'Segoe UI', Helvetica, Arial, sans-serif; fill: {ACCENT_COLOR}; }}
    </style>
  </defs>

  <!-- Card background -->
  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="12" fill="{BG_COLOR}" stroke="{BORDER_COLOR}" stroke-width="1"/>

  <!-- Header -->
  <text x="30" y="38" class="logo">THE ODIN PROJECT</text>
  <text x="30" y="64" class="title">{course}</text>

  <!-- Current lesson -->
  <text x="30" y="86" class="label">Current lesson</text>
  <text x="160" y="86" class="value">{lesson}</text>

  <!-- Progress bar track -->
  <rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="7" fill="{TRACK_COLOR}"/>
  <!-- Progress bar fill -->
  <rect x="{bar_x}" y="{bar_y}" width="{fill_w}" height="{bar_h}" rx="7" fill="url(#barGradient)"/>
  <!-- Percent label -->
  <text x="{WIDTH - 30}" y="{bar_y - 6}" text-anchor="end" class="pct">{percent}% complete</text>

  <!-- Projects completed -->
  <text x="30" y="138" class="label">Projects completed</text>
  <text x="220" y="138" class="value">{proj_done} / {proj_total}</text>

  <!-- Divider -->
  <line x1="30" y1="156" x2="{WIDTH - 30}" y2="156" stroke="{BORDER_COLOR}" stroke-width="1"/>

  <!-- Footer -->
  <text x="30" y="178" class="footer">Last updated: {last_updated}</text>
  <text x="{WIDTH - 30}" y="178" text-anchor="end" class="footer">theodinproject.com</text>
</svg>
'''
    return svg


def main():
    data = load_progress(INPUT_FILE)
    svg = build_svg(data)
    with open(OUTPUT_FILE, "w") as f:
        f.write(svg)
    print(f"Generated {OUTPUT_FILE} from {INPUT_FILE}")


if __name__ == "__main__":
    main()
