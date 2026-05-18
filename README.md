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

# wooden-roll
cd ../wooden-roll
npm install
./setup.sh
```

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

Drop royalty-free `.mp3` tracks into:

```
music/motivational/
music/calm/
music/uplifting/
```

Sources: [Pixabay Music](https://pixabay.com/music/), [Free Music Archive](https://freemusicarchive.org/), [YouTube Audio Library](https://studio.youtube.com)

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

### Render a specific config

```bash
python3 main.py output/configs/my_config.yaml
```

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

---

## Project structure

```
.claude/commands/        # Claude Code skills
config/settings.yaml     # pipeline settings
data/used_photos.json    # Pexels dedup tracker
music/                   # local music tracks
output/
  texts/                 # generated text batches
  configs/               # wooden-roll YAMLs
  videos/                # rendered shorts
  approved/              # videos ready to upload
  uploaded/              # uploaded videos
pipeline/                # Python modules
main.py                  # pipeline entry point
```
