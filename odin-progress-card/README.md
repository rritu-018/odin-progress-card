# Odin Project Progress Card

A dark-themed, dynamically-generated SVG card showing your progress through
[The Odin Project](https://www.theodinproject.com/), styled similarly to a
boot.dev profile card. Designed to be embedded in your GitHub profile README.

Since The Odin Project has no public API or profile page to pull stats from
automatically, this card uses a tiny manual data file (`progress.json`) that
you update by hand — it takes about 10 seconds. A GitHub Action then
regenerates the SVG and commits it automatically, so you never have to run
any script yourself.

## How it works

1. `progress.json` — you edit this with your current stats.
2. `generate_card.py` — reads that file and renders `odin_progress_card.svg`.
3. `.github/workflows/update-card.yml` — a GitHub Action that:
   - runs automatically whenever you push a change to `progress.json`
   - also runs once a week on its own, so the "last updated" date and card
     never go stale even if you forget to push
   - regenerates the SVG and commits it back to the repo for you

## Setup (one-time)

1. Create a new GitHub repo (e.g. `odin-progress-card`) — public, so the
   raw SVG URL works in your profile README.
2. Push these files to it:
   - `progress.json`
   - `generate_card.py`
   - `.github/workflows/update-card.yml`
3. In your **profile README** repo (the special repo named exactly like your
   GitHub username), add this line wherever you want the card to appear:

   ```markdown
   ![Odin Project Progress](https://raw.githubusercontent.com/<your-username>/odin-progress-card/main/odin_progress_card.svg)
   ```

   Replace `<your-username>` and the repo name if you called it something
   else.

4. Commit, push, and check your profile — the card should appear.

## Updating your progress

Whenever you finish a lesson or project, open `progress.json` and edit the
relevant field(s):

```json
{
  "course": "Full Stack JavaScript",
  "percent_complete": 42,
  "current_lesson": "Working with APIs",
  "projects_completed": 9,
  "projects_total": 24,
  "last_updated": "2026-06-21"
}
```

Push the change. The GitHub Action picks it up, regenerates the card, and
commits the new SVG — usually within a minute. Your profile README will
show the updated card the next time it's loaded (GitHub may cache the raw
SVG for a few minutes on their CDN, so don't worry if it takes a moment).

## Customizing the look

All colors, sizing, and fonts live at the top of `generate_card.py` under
the `---- Card dimensions & theme ----` section. Tweak `ACCENT_COLOR`,
`BG_COLOR`, etc. and re-run the script (or just push — the Action will
re-render it for you).

## Running it locally (optional)

```bash
python3 generate_card.py
```

This reads `progress.json` and writes `odin_progress_card.svg` in the same
folder, so you can preview changes before pushing.
