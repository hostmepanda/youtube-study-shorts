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

### Approve a video for upload

Move it to `output/approved/`:

```bash
mv output/videos/short_YYYYMMDD_HHMMSS.mp4 output/approved/
```

### Upload approved videos

```bash
python3 pipeline/youtube_uploader.py
```

Uploads each video in `output/approved/`, schedules at 9am on consecutive days, moves to `output/uploaded/`.

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
.claude/commands/        # Claude Code skills (/generate-texts, /generate-short)
config/settings.yaml     # pipeline settings
data/used_photos.json    # Pexels dedup tracker
music/                   # local music tracks (by mood)
output/
  texts/                 # generated text batches + used_texts.json
  configs/               # wooden-roll YAMLs + metadata sidecars
  videos/                # rendered shorts
  approved/              # videos ready to upload
  uploaded/              # uploaded videos
pipeline/                # Python modules
  config_builder.py      # builds wooden-roll YAML from text/images/music
  image_fetcher.py       # fetches Pexels images
  music_selector.py      # picks a track by mood
  youtube_uploader.py    # schedules and uploads to YouTube
main.py                  # pipeline entry point
```

---

## Disk cleanup

### Safe to delete

| Path | Why it's safe |
|------|---------------|
| `output/videos/` | Raw renders — once moved to `approved/` or reviewed, no longer needed |
| `output/configs/` | YAML + metadata sidecars — regenerated on every run |
| `output/images/` | Pexels images — deleted automatically after each render; any leftovers are safe to remove |

```bash
rm -rf output/videos/ output/configs/ output/images/
```

### Never delete

| Path | Why you must keep it |
|------|----------------------|
| `output/texts/used_texts.json` | Tracks which texts have already been used. Delete this and the pipeline will re-use already-published content. |
| `output/texts/batch_*.json` | Source text batches — the content library |
| `output/texts/parables_*.json` | Source parable batches — the content library |
| `output/approved/` | Videos queued for upload — delete only after uploading |
| `output/uploaded/` | Archive of uploaded videos — safe to delete if you don't need local copies |

---

## Voice cloning details

Voice cloning uses [KokoClone](https://github.com/Ashish-Patnaik/kokoclone) with the Kanade voice conversion model. It runs as an optional post-processing step after Kokoro TTS — subtitle timing is preserved.

The Kokoro voice (e.g. `am_eric`) is used only as an intermediate source for conversion. The final audio reflects your reference voice only.

`CLONE_VOICE_PATH` can also be set permanently in `.env` to always use voice cloning.
