# YouTube Study Shorts

Automated pipeline for generating motivational YouTube Shorts on language learning.

## Setup

### 1. Clone repos

```bash
git clone https://github.com/hostmepanda/youtube-study-shorts
git clone https://github.com/hostmepanda/wooden-roll   # must be at ../wooden-roll
git clone https://github.com/Ashish-Patnaik/kokoclone  # must be at ../kokoclone
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
python3 pipeline/youtube_uploader.py --auth
```

This opens a browser, asks you to log in, then saves `token.json`. After this you won't need to re-authenticate.

> `credentials.json` and `token.json` are gitignored — never commit them.

### 5. Add music

Drop royalty-free `.mp3` tracks into mood subfolders:

```
music/motivational/
music/calm/
music/uplifting/
```

Sources: [Pixabay Music](https://pixabay.com/music/), [Free Music Archive](https://freemusicarchive.org/), [YouTube Audio Library](https://studio.youtube.com)

Or generate tracks locally with MusicGen (requires `../mlx-examples`):

```bash
python3 ../wooden-roll/scripts/generate_music.py --mood motivational --count 3 --output-dir music/motivational
```

---

## Usage

### Generate a batch of 10 texts

```bash
/generate-texts   # Claude Code skill
```

### Generate one short (full pipeline)

```bash
python3 main.py
```

### Generate with your cloned voice

Voice cloning is configured in `config/settings.yaml`:

```yaml
voice:
  custom_voice: voice/elevenlabs_reference.wav  # relative to project root
```

When `custom_voice` is set and the file exists, every generated short uses Kanade voice conversion. To disable cloning, comment out or remove the `custom_voice` line.

To override for a single run without changing the config:

```bash
CLONE_VOICE_PATH=/path/to/your_voice.wav python3 main.py
```

`CLONE_VOICE_PATH` always takes priority over `settings.yaml`. The pipeline generates TTS with Kokoro first (for subtitle timing), then applies Kanade voice conversion.

### Render a specific config (regenerate video)

Pass the config path to skip image fetching, music selection, and text picking — goes straight to audio + video rendering:

```bash
python3 main.py output/configs/parable_YYYYMMDD_HHMMSS.yaml
```

Useful when you want to re-render a video without generating a new one from scratch.

### iCloud copy

After every render, `main.py` automatically copies the video to:

```
/Users/panda/Library/Mobile Documents/com~apple~CloudDocs/Experiments/Youtube-shorts/output/
```

A warning is printed reminding you that the file exists in **two places** — local `output/videos/` and iCloud. Delete both when no longer needed.

### Publish lifecycle

Every render produces one yaml file at `formats/<format>/configs/new/<id>.yaml`, carrying its own `youtube:` metadata block (title/description/tags) — no separate meta.json. The rendered `.mp4` lives permanently in `output/videos/` and is never moved; only the yaml travels:

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
python3 pipeline/youtube_uploader.py
```

Uploads everything sitting in any `formats/*/configs/waiting_upload/`. Schedule by format, US Eastern Time, one per day starting today:

| Format | Publish time |
|--------|-------------|
| `short-motivation` | 09:00 ET |
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
python3 pipeline/thumbnail_generator.py \
  --lines "Line 1." "Line 2" "gold line." \
  --output preview.jpg
```

### Automatic upload via launchd (macOS)

A launchd agent runs the uploader automatically at **06:00, 12:00, and 18:00** every day.

Plist: `~/Library/LaunchAgents/com.studygotogether.uploader.plist`
Logs: `logs/uploader.log` / `logs/uploader.error.log`

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
.claude/commands/        # Claude Code skills (/generate-texts, /generate-short, /publish, /clean-artifacts...)
config/settings.yaml     # pipeline settings
data/used_photos.json    # Pexels dedup tracker
music/                   # local music tracks (by mood)
formats/
  short-motivation/      # plain motivational texts (text_NNN)
  parable-classic/       # Zen-style human parables (classic_NNN)
  parable-animal/        # absurdist animal parables (animal_NNN)
  legacy/                # pre-restructure parable_NNN content lifecycle only
  <format>/
    topics.md            # style rules, topic pool, "already used" tracking (curated, human/LLM-read)
    used.json            # dedup tracker (machine-read by main.py's picker)
    drafts/              # generated batches not yet rendered
    configs/
      new/               # just rendered, not yet queued
      waiting_upload/    # queued — python3 pipeline/youtube_uploader.py picks these up
      archive/           # already uploaded
output/
  texts/                 # legacy text/parable batches + used_texts.json (pre-restructure content)
  videos/                # rendered videos — PERMANENT home, never moved or deleted
  images/                # transient Pexels image cache, auto-cleaned after each render
pipeline/                # Python modules
  config_builder.py      # builds wooden-roll YAML (+ embedded youtube: metadata) from text/images/music
  image_fetcher.py       # fetches Pexels images
  music_selector.py      # picks a track by mood
  youtube_uploader.py    # uploads everything in formats/*/configs/waiting_upload/
main.py                  # pipeline entry point — also cleans render scratch after each success
```

---

## Disk cleanup

`main.py` auto-cleans render scratch (wooden-roll's per-render audio/video cache, downloaded images) right after every successful render — see `/clean-artifacts` for cleaning up leftovers from interrupted runs and orphaned pre-restructure debris.

**`output/videos/*.mp4` is permanent and is never deleted by any tooling here** — only the yaml lifecycle file moves between `new/` → `waiting_upload/` → `archive/`, the video itself stays put.

| Path | Why you must keep it |
|------|----------------------|
| `output/texts/used_texts.json`, `formats/*/used.json` | Dedup trackers. Delete and the pipeline will re-use already-published content. |
| `output/texts/batch_*.json`, `output/texts/parables_*.json`, `formats/*/drafts/*.json` | Source content library |
| `formats/*/topics.md` | Curated topic pools + "avoid repeating" tracking |
| `output/videos/` | Permanent video archive |

---

## Voice cloning details

Voice cloning uses [KokoClone](https://github.com/Ashish-Patnaik/kokoclone) with the Kanade voice conversion model. It runs as an optional post-processing step after Kokoro TTS — subtitle timing is preserved.

The Kokoro voice (e.g. `am_eric`) is used only as an intermediate source for conversion. The final audio reflects your reference voice only.

`CLONE_VOICE_PATH` can also be set permanently in `.env` to always use voice cloning.
