#!/usr/bin/env python3
"""
generate_card.py

Reads progress.json and renders an RPG-styled, dark/navy SVG card for
The Odin Project, inspired by a boot.dev-style profile card: name in a
serif display font, a level/rank badge derived from percent_complete,
an avatar circle, lessons/projects stats, and a joined date.

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

# ---- Card dimensions ----
WIDTH = 700
HEIGHT = 360

# ---- Theme (navy / textured-RPG-card inspired) ----
BG_TOP = "#1b2735"
BG_BOTTOM = "#0f1822"
BORDER_COLOR = "#3a4a5c"
ACCENT_GOLD = "#d4af37"
ACCENT_GOLD_LIGHT = "#f3d27a"
TEXT_PRIMARY = "#f5f1e8"
TEXT_SECONDARY = "#9aa7b5"
TEXT_MUTED = "#6b7785"
TRACK_COLOR = "#0b1117"
BAR_GRADIENT_START = "#d4af37"
BAR_GRADIENT_END = "#e8743b"
AVATAR_BG = "#2a3848"
AVATAR_RING = "#d4af37"


# ---- Rank thresholds, derived from percent_complete ----
RANKS = [
    (0, 10, "Wanderer"),
    (10, 25, "Novice"),
    (25, 45, "Apprentice"),
    (45, 65, "Journeyman"),
    (65, 85, "Adept"),
    (85, 100, "Master"),
    (100, 101, "Odin Graduate"),
]


def load_progress(path):
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Could not find {path}. Create it with the required fields "
            "(see README.md)."
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


def rank_for_percent(percent):
    for lo, hi, title in RANKS:
        if lo <= percent < hi:
            return title
    return RANKS[-1][2]


def level_for_percent(percent):
    # Simple mapping: level 1-20, scaling with percent complete.
    # Never shows level 0 even at 0% progress, mirrors boot.dev's
    # "everyone starts at lvl 1" feel.
    return max(1, round(percent / 5))


def build_svg(data):
    name = escape_xml(data.get("name", "Anonymous Learner"))
    username = escape_xml(data.get("github_username", ""))
    started = format_date(data.get("started_date", ""))
    course = escape_xml(data.get("course", "The Odin Project"))
    percent = data.get("percent_complete", 0)
    percent = max(0, min(100, percent))
    lesson = escape_xml(data.get("current_lesson", "\u2014"))
    lessons_done = data.get("lessons_completed", 0)
    proj_done = data.get("projects_completed", 0)
    proj_total = data.get("projects_total", 0)
    last_updated = format_date(data.get("last_updated", ""))

    rank = rank_for_percent(percent)
    level = level_for_percent(percent)

    # Progress bar geometry
    bar_x = 40
    bar_y = 296
    bar_w = WIDTH - 80
    bar_h = 12
    fill_w = round(bar_w * (percent / 100))

    avatar_cx = 590
    avatar_cy = 110
    avatar_r = 58
    avatar_url = f"https://github.com/{username}.png?size=200" if username else None

    if avatar_url:
        avatar_markup = (
            f'<image href="{escape_xml(avatar_url)}" '
            f'x="{avatar_cx - avatar_r}" y="{avatar_cy - avatar_r}" '
            f'width="{avatar_r * 2}" height="{avatar_r * 2}" '
            f'clip-path="url(#avatarClip)" preserveAspectRatio="xMidYMid slice"/>'
        )
    else:
        avatar_markup = (
            f'<circle cx="{avatar_cx}" cy="{avatar_cy - 14}" r="22" fill="{TEXT_MUTED}" opacity="0.55"/>'
            f'<path d="M {avatar_cx - 38} {avatar_cy + 50} Q {avatar_cx} {avatar_cy + 6} '
            f'{avatar_cx + 38} {avatar_cy + 50} L {avatar_cx + 38} {avatar_cy + avatar_r} '
            f'L {avatar_cx - 38} {avatar_cy + avatar_r} Z" fill="{TEXT_MUTED}" opacity="0.55"/>'
        )

    svg = f'''<svg width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The Odin Project RPG progress card">
  <defs>
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="40%" y2="100%">
      <stop offset="0%" stop-color="{BG_TOP}"/>
      <stop offset="100%" stop-color="{BG_BOTTOM}"/>
    </linearGradient>
    <linearGradient id="barGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{BAR_GRADIENT_START}"/>
      <stop offset="100%" stop-color="{BAR_GRADIENT_END}"/>
    </linearGradient>
    <radialGradient id="avatarGradient" cx="35%" cy="30%" r="75%">
      <stop offset="0%" stop-color="#3d4f63"/>
      <stop offset="100%" stop-color="{AVATAR_BG}"/>
    </radialGradient>
    <clipPath id="avatarClip">
      <circle cx="{avatar_cx}" cy="{avatar_cy}" r="{avatar_r}"/>
    </clipPath>
    <filter id="paperTexture" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" result="noise" seed="7"/>
      <feColorMatrix in="noise" type="matrix"
        values="0 0 0 0 0
                0 0 0 0 0
                0 0 0 0 0
                0 0 0 0.04 0"/>
      <feComposite operator="over" in2="SourceGraphic"/>
    </filter>
    <style>
      .name {{ font: 700 34px Georgia, 'Times New Roman', serif; fill: {TEXT_PRIMARY}; }}
      .handle {{ font: 400 15px 'Segoe UI', Helvetica, Arial, sans-serif; fill: {TEXT_SECONDARY}; }}
      .level-num {{ font: 700 32px Georgia, serif; fill: {ACCENT_GOLD_LIGHT}; }}
      .level-unit {{ font: 600 14px 'Segoe UI', Helvetica, Arial, sans-serif; fill: {TEXT_SECONDARY}; }}
      .rank {{ font: italic 400 17px Georgia, serif; fill: {TEXT_SECONDARY}; }}
      .stat-num {{ font: 700 26px Georgia, serif; fill: {TEXT_PRIMARY}; }}
      .stat-label {{ font: 400 14px 'Segoe UI', Helvetica, Arial, sans-serif; fill: {TEXT_SECONDARY}; }}
      .lesson-label {{ font: 600 12px 'Segoe UI', Helvetica, Arial, sans-serif; fill: {TEXT_MUTED}; letter-spacing: 1px; }}
      .lesson-value {{ font: 600 14px 'Segoe UI', Helvetica, Arial, sans-serif; fill: {TEXT_PRIMARY}; }}
      .pct {{ font: 700 13px 'Segoe UI', Helvetica, Arial, sans-serif; fill: {TEXT_PRIMARY}; }}
      .footer {{ font: 400 12px 'Segoe UI', Helvetica, Arial, sans-serif; fill: {TEXT_MUTED}; }}
      .badge-text {{ font: 700 13px Georgia, serif; fill: {ACCENT_GOLD_LIGHT}; }}
    </style>
  </defs>

  <!-- Card background -->
  <rect x="1" y="1" width="{WIDTH - 2}" height="{HEIGHT - 2}" rx="14" fill="url(#bgGradient)" stroke="{BORDER_COLOR}" stroke-width="2"/>
  <rect x="1" y="1" width="{WIDTH - 2}" height="{HEIGHT - 2}" rx="14" filter="url(#paperTexture)" opacity="0.5"/>

  <!-- Inner border accent -->
  <rect x="14" y="14" width="{WIDTH - 28}" height="{HEIGHT - 28}" rx="10" fill="none" stroke="{ACCENT_GOLD}" stroke-width="1" opacity="0.35"/>

  <!-- Name + handle -->
  <text x="40" y="78" class="name">{name}</text>
  <text x="40" y="104" class="handle">@{username}</text>

  <!-- Level -->
  <text x="40" y="168" class="level-num">{level}</text>
  <text x="68" y="168" class="level-unit">lvl</text>
  <text x="40" y="194" class="rank">{rank}</text>

  <!-- Avatar circle -->
  <circle cx="{avatar_cx}" cy="{avatar_cy}" r="{avatar_r + 5}" fill="none" stroke="{AVATAR_RING}" stroke-width="3" opacity="0.85"/>
  <circle cx="{avatar_cx}" cy="{avatar_cy}" r="{avatar_r}" fill="url(#avatarGradient)"/>
  {avatar_markup}

  <!-- Joined date + course badge under avatar -->
  <text x="{avatar_cx}" y="190" text-anchor="middle" class="footer">Started: {started}</text>
  <rect x="{avatar_cx - 70}" y="200" width="140" height="26" rx="6" fill="#0b1117" stroke="{ACCENT_GOLD}" stroke-width="1" opacity="0.9"/>
  <text x="{avatar_cx}" y="217" text-anchor="middle" class="badge-text">ODIN PROJECT</text>

  <!-- Lessons / Course stats row -->
  <text x="40" y="236" class="stat-num">{lessons_done}</text>
  <text x="{40 + 14 * len(str(lessons_done)) + 14}" y="236" class="stat-label">Lessons</text>

  <text x="220" y="236" class="stat-num">{proj_done}/{proj_total}</text>
  <text x="{220 + 16 * len(f"{proj_done}/{proj_total}") + 14}" y="236" class="stat-label">Projects</text>

  <!-- Current course + lesson -->
  <text x="40" y="266" class="lesson-label">CURRENT COURSE</text>
  <text x="220" y="266" class="lesson-value">{course} \u2014 {lesson}</text>

  <!-- Progress bar label -->
  <text x="{WIDTH - 40}" y="{bar_y - 16}" text-anchor="end" class="pct">{percent}% to graduation</text>

  <!-- Progress bar track -->
  <rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="6" fill="{TRACK_COLOR}" stroke="{BORDER_COLOR}" stroke-width="1"/>
  <!-- Progress bar fill -->
  <rect x="{bar_x}" y="{bar_y}" width="{fill_w}" height="{bar_h}" rx="6" fill="url(#barGradient)"/>

  <!-- Divider -->
  <line x1="40" y1="318" x2="{WIDTH - 40}" y2="318" stroke="{BORDER_COLOR}" stroke-width="1"/>

  <!-- Footer -->
  <text x="40" y="340" class="footer">Last updated: {last_updated}</text>
  <text x="{WIDTH - 40}" y="340" text-anchor="end" class="footer">theodinproject.com</text>
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
