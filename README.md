# YouTube Study Shorts

Automated pipeline for generating motivational YouTube Shorts on language learning.

## Setup

### 1. Clone repos

```bash
git clone https://github.com/hostmepanda/youtube-study-shorts
git clone https://github.com/hostmepanda/wooden-roll   # must be at ../wooden-roll
```

### 2. Install dependencies

```bash
# Python
pip3 install -r requirements.txt

# wooden-roll (Python 3.13 required)
cd ../wooden-roll
npm install
python3.13 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

> wooden-roll requires Python 3.13 for `kanade-tokenizer` (voice cloning). If `python3.13` is not in PATH, use the full path e.g. `/opt/homebrew/opt/python@3.13/bin/python3.13`.

### 3. Environment variables

```bash
cp .env.example .env
```

Fill in `.env`:

```env
PEXELS_API_KEY=        # pexels.com/api → Get Started
PREMISS_API_KEY=       # Premiss TTS API key
YOUTUBE_CLIENT_ID=     # see below
YOUTUBE_CLIENT_SECRET= # see below
YOUTUBE_REFRESH_TOKEN= # generated after first OAuth login
```

### 4. YouTube credentials

**Create a Google Cloud project:**

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. **Select a project** → **New Project** → name it `youtube-shorts-pipeline` → **Create**

**Enable YouTube Data API:**

1. **APIs & Services** → **Library**
2. Search `YouTube Data API v3` → **Enable**

**Create OAuth client:**

1. **APIs & Services** → **Credentials** → **Create Credentials** → **OAuth client ID**
2. If prompted: configure consent screen → **External** → fill app name + your email → **Save**
3. Application type: **Desktop app** → Name: `shorts-pipeline` → **Create**
4. **Download JSON** → save as `credentials.json` in the project root

**Add yourself as test user:**

1. **APIs & Services** → **OAuth consent screen**
2. Scroll to **Test users** → **Add users** → add your Gmail

**Authenticate (first time only):**

```bash
python3 src/pipeline/youtube_uploader.py --auth
```

This opens a browser, asks you to log in, then saves `token.json`. After this you won't need to re-authenticate.

> `credentials.json` and `token.json` are gitignored — never commit them.

### 5. Add music

Drop royalty-free `.mp3` tracks into mood subfolders:

```
music/motivational/
music/calm/
music/uplifting/
music/parable/
music/long/
```

Sources: [Pixabay Music](https://pixabay.com/music/), [Free Music Archive](https://freemusicarchive.org/), [YouTube Audio Library](https://studio.youtube.com)

---

## Usage

### Generate a batch of 10 motivational texts

```bash
/generate-texts   # Claude Code skill
```

### Generate one short (full pipeline)

```bash
python3 main.py
```

### Render a specific config (regenerate video)

Pass the config path to skip everything except audio + video rendering:

```bash
python3 main.py formats/short-motivation/configs/new/text_YYYYMMDD_HHMMSS.yaml
```

### iCloud copy

After every render, `main.py` automatically copies the video to:

```
/Users/panda/Library/Mobile Documents/com~apple~CloudDocs/Experiments/Youtube-shorts/output/
```

A warning is printed reminding you that the file exists in **two places** — local `output/videos/` and iCloud.

### Publish lifecycle

Every render produces one yaml file at `formats/<format>/configs/new/<id>.yaml`, carrying its own `youtube:` metadata block (title/description/tags/category_id/video_path) — no separate meta.json. The rendered `.mp4` lives permanently in `output/videos/` and is never moved; only the yaml travels:

```
formats/<format>/configs/new/  →  waiting_upload/  →  archive/
```

Queue a video for upload by moving its yaml:

```bash
mv formats/parable-classic/configs/new/classic_YYYYMMDD_HHMMSS.yaml \
   formats/parable-classic/configs/waiting_upload/
```

### Upload queued videos

```bash
python3 src/pipeline/youtube_uploader.py
```

Uploads everything sitting in any `formats/*/configs/waiting_upload/`. Schedule by format, US Eastern Time, one per day starting today:

| Format | Publish time |
|--------|-------------|
| `short-motivation` | 09:00 ET (slot 1) / 19:00 ET (slot 2 when >1/day) |
| `long-monologue` | 12:00 ET |
| parables + legacy | 16:30 ET |

On success, each yaml moves to `archive/` — the mp4 is untouched.

### Thumbnails for long-monologue

The uploader auto-generates a branded thumbnail from the hook lines in `youtube.hook`:

```yaml
youtube:
  hook:
    - "He was in prison."
    - "He chose to learn"
    - "their language."
```

To preview a thumbnail manually:

```bash
python3 src/pipeline/thumbnail_generator.py \
  --lines "Line 1." "Line 2" "gold line." \
  --output preview.jpg
```

### Automatic upload via launchd (macOS)

A launchd agent runs the uploader automatically at **06:00, 12:00, and 18:00** every day.

Plist: `src/scripts/com.studygotogether.uploader.plist`

```bash
# Load (enable)
launchctl load ~/Library/LaunchAgents/com.studygotogether.uploader.plist

# Unload (disable)
launchctl unload ~/Library/LaunchAgents/com.studygotogether.uploader.plist

# Check status
launchctl list | grep studygotogether
```

---

## Project structure

```
.claude/commands/        # Claude Code skills (/generate-texts, /generate-short, /publish, ...)
formats/
  short-motivation/      # plain motivational texts (text_NNN)
  parable-classic/       # Zen-style human parables (classic_NNN)
  parable-animal/        # absurdist animal parables (animal_NNN)
  long-monologue/        # long-form video scripts (longmono_NNN)
  legacy/                # pre-restructure parable_NNN content (lifecycle only)
  <format>/
    topics.md            # style rules, topic pool, "already used" tracking
    used.json            # dedup tracker (machine-read by main.py)
    drafts/              # generated batches not yet rendered
    configs/
      new/               # just rendered, not yet queued
      waiting_upload/    # queued — src/pipeline/youtube_uploader.py picks these up
      archive/           # already uploaded
music/
  motivational/          # upbeat tracks for motivation shorts
  calm/                  # calm tracks
  uplifting/             # uplifting tracks
  parable/               # tracks for parables
  long/                  # tracks for long-form videos
output/
  videos/                # rendered videos — PERMANENT home, never moved or deleted
src/
  config/
    settings.yaml        # pipeline settings (voice, Premiss, music mood, etc.)
  pipeline/
    config_builder.py    # builds wooden-roll YAML + embedded youtube: metadata
    image_fetcher.py     # fetches Pexels background images
    music_selector.py    # picks a track by mood
    thumbnail_generator.py  # generates branded 1280×720 thumbnail for long-form
    youtube_uploader.py  # uploads everything in formats/*/configs/waiting_upload/
  scripts/
    daily_generate.sh    # launchd daily run: upload queued + generate new
    com.studygotogether.uploader.plist  # macOS launchd agent definition
experiments/
  duck-lesson/           # one-off duck lesson video experiment
voice/                   # reference wav files for voice cloning
main.py                  # pipeline entry point — cleans render scratch after each success
schedule.md              # publishing schedule (auto-updated on each upload)
CLAUDE.md                # project instructions for Claude Code
```

---

## Generate animal parables via Premiss

Animal parables use a two-step pipeline:

**Step 1 — generate plot seeds:**

```bash
python3 formats/parable-animal/pipeline/generate_seeds.py [N]
# default N = 10
```

Seeds are saved to `formats/parable-animal/seeds.json`. Review and edit before proceeding.

**Step 2 — generate a full parable from the next pending seed:**

```bash
python3 formats/parable-animal/pipeline/generate_parable.py [seed_id]
# omit seed_id to pick the first pending seed automatically
```

Saves to `formats/parable-animal/drafts/parables_YYYYMMDD_HHMMSS.json` and marks the seed as used. Then run `python3 main.py` to render it.

Voice for parables: set `premiss.voice` in `src/config/settings.yaml`. Options: `elder` (default), `abbot`, `thomas`.

---

## Disk cleanup

`main.py` auto-cleans render scratch (wooden-roll's per-render audio/video cache, downloaded images) right after every successful render — see `/clean-artifacts` for cleaning up leftovers from interrupted runs.

**`output/videos/*.mp4` is permanent and is never deleted by any tooling here** — only the yaml lifecycle file moves between `new/` → `waiting_upload/` → `archive/`, the video stays put.

| Path | Why you must keep it |
|------|----------------------|
| `formats/*/used.json` | Dedup trackers — delete and the pipeline will re-use already-published content |
| `formats/*/drafts/*.json` | Source content library |
| `formats/*/topics.md` | Curated topic pools + "avoid repeating" tracking |
| `output/videos/` | Permanent video archive |
