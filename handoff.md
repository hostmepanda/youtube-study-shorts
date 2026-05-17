# Shorts Pipeline — Handoff для Claude Code

## Контекст

Автоматизированный конвейер для генерации мотивационных YouTube Shorts на тему **изучения языков**.
Пайплайн должен работать по расписанию и производить готовые видео с минимальным участием человека.

---

## Стек (обсуждён, утверждён)

- **Python** — основной язык пайплайна
- **Claude API** (`claude-sonnet-4-20250514`) — генерация текстов для слайдов
- **Pexels API** — бесплатные стоковые фото (royalty-free)
- **FFmpeg** — сборка видео из слайдов + музыка
- **YouTube Data API v3** — публикация (официальный, не Selenium)
- **YAML** — конфиг для каждого шорта
- **Cron / GitHub Actions** — запуск по расписанию

---

## Архитектура пайплайна

```
scheduler (cron/GH Actions)
        │
        ▼
1. text_generator.py       ← Claude API → тексты для слайдов
        │
        ▼
2. image_fetcher.py        ← Pexels API → фото по ключевым словам
        │
        ▼
3. music_selector.py       ← локальная папка /music → рандом по тегу настроения
        │
        ▼
4. config_builder.py       ← собирает YAML конфиг шорта
        │
        ▼
5. video_renderer.py       ← FFmpeg читает YAML → рендерит .mp4 (9:16)
        │
        ▼
6. youtube_uploader.py     ← YouTube Data API v3 → публикация
```

---

## Модуль 1 — Генерация текстов (Claude API)

### Стиль текстов (утверждён в диалоге)

Прямой, честный, без агрессии, с каплей тепла. Не детский, не философский, не мягкий.

**Эталонный пример:**
```
Ошибиться — это нормально.
Молчать из страха — нет.
Говори. Ошибайся. Становись лучше.
```

**Другие утверждённые примеры:**
```
Язык — это инструмент.
Его не нужно совершенствовать вечно.
Его нужно использовать.
```
```
Молоток может быть простым или титановым.
Но гвоздь забивает любой.
Хватит выбирать — начни строить.
```
```
Учить язык и не говорить —
всё равно что сажать и никогда не собирать урожай.
Открой рот. Пора собирать.
```

### Промпт для генерации

```python
SYSTEM_PROMPT = """
Ты пишешь короткие мотивационные тексты для YouTube Shorts на тему изучения языков.

Стиль: прямой, честный, без агрессии, с каплей тепла и веры в человека.
НЕ: детский, сюсюкающий, философский, грубый, корпоративный.

Структура текста: 3 строки. Первые две — факт или провокация. Третья — призыв или вывод.
Каждая строка короткая. Без лишних слов.

Отвечай только текстом. Никаких пояснений, никакого markdown.
"""
```

### Выходной формат

```python
# Генерировать пачками по 10 штук
# Сохранять в texts/batch_YYYYMMDD.json
[
  {
    "id": "text_001",
    "lines": ["Строка 1", "Строка 2", "Строка 3"],
    "mood": "motivational",  # для подбора музыки
    "keywords": ["mistakes", "speaking", "progress"]  # для подбора фото
  }
]
```

---

## Модуль 2 — Фотографии (Pexels API)

### Логика выбора

- Запрос по `keywords` из текстового блока
- Фильтр: горизонталь ИЛИ вертикаль (для 9:16 кропим центр)
- Минимальное разрешение: 1080x1920 или кроп из большего
- Не брать одно фото дважды → вести `used_photos.json`

### Ключевые слова по темам

```python
KEYWORD_POOLS = {
    "mistakes": ["learning", "growth", "challenge", "perseverance"],
    "speaking": ["conversation", "communication", "people talking"],
    "progress": ["path", "journey", "sunrise", "running"],
    "language": ["books", "travel", "world map", "city"]
}
```

### API

```python
# GET https://api.pexels.com/v1/search?query={keyword}&per_page=15&orientation=portrait
# Header: Authorization: {PEXELS_API_KEY}
```

---

## Модуль 3 — Музыка

### Подход: локальная папка

```
/music
  /motivational/   ← энергичная, BPM 100-130
  /calm/           ← спокойная, BPM 60-90
  /uplifting/      ← воодушевляющая, BPM 90-110
```

Выбор трека: рандом из папки соответствующей `mood` текстового блока.

### Источники (royalty-free, YouTube-safe)

- **Pixabay Music** — бесплатно, скачать вручную
- **Free Music Archive** — бесплатно
- **YouTube Audio Library** — бесплатно, прямо в Studio

> ⚠️ Epidemic Sound и подобные — платные подписки, подключить позже если нужно.

---

## Модуль 4 — YAML конфиг и сборка видео

### Пример YAML конфига

```yaml
short:
  id: "short_20240315_001"
  duration: 15  # секунд
  resolution: "1080x1920"  # 9:16

  slides:
    - text: "Ошибиться — это нормально."
      font_size: 64
      position: center
      duration: 4
    - text: "Молчать из страха — нет."
      font_size: 64
      position: center
      duration: 4
    - text: "Говори. Ошибайся.\nСтановись лучше."
      font_size: 58
      position: center
      duration: 7

  image: "images/forest_path_001.jpg"
  music: "music/motivational/track_03.mp3"
  music_volume: 0.4

  metadata:
    title: "Не бойся ошибаться #изучениеязыков #мотивация"
    description: "Каждая ошибка приближает тебя к свободному владению языком."
    tags: ["изучениеязыков", "motivation", "language learning", "shorts"]
    category_id: "27"  # Education
```

### FFmpeg команда (базовая)

```bash
ffmpeg \
  -loop 1 -i image.jpg \
  -i music.mp3 \
  -vf "scale=1080:1920,drawtext=..." \
  -t 15 \
  -shortest \
  output.mp4
```

> Детальную реализацию `drawtext` с анимацией написать в `video_renderer.py`

---

## Модуль 5 — Публикация (YouTube Data API v3)

### Квоты

| Операция | Units |
|----------|-------|
| Загрузка видео | 1600 |
| Дневной лимит | 10000 |
| **Максимум видео/день** | **6** |

### Рекомендуемый режим

**Полуавтомат для старта:**
- Пайплайн генерирует видео + заголовки + описания
- Человек загружает вручную раз в неделю
- Переход на полный автомат после набора истории канала

**Полный автомат (позже):**
- Рандомизация времени публикации ±1-2 часа от целевого
- Не публиковать более 1 видео в день
- OAuth2 авторизация (не API key)

### Пример загрузки

```python
youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": config["metadata"]["title"],
            "description": config["metadata"]["description"],
            "tags": config["metadata"]["tags"],
            "categoryId": config["metadata"]["category_id"]
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    },
    media_body=MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)
).execute()
```

---

## Структура репозитория

```
shorts-pipeline/
├── config/
│   └── settings.yaml          # API ключи, пути, настройки
├── pipeline/
│   ├── text_generator.py
│   ├── image_fetcher.py
│   ├── music_selector.py
│   ├── config_builder.py
│   ├── video_renderer.py
│   └── youtube_uploader.py
├── music/
│   ├── motivational/
│   ├── calm/
│   └── uplifting/
├── output/
│   ├── texts/
│   ├── images/
│   ├── configs/
│   └── videos/
├── data/
│   └── used_photos.json       # дедупликация фото
├── main.py                    # точка входа
├── requirements.txt
└── .github/
    └── workflows/
        └── daily_run.yml      # GitHub Actions расписание
```

---

## Переменные окружения

```env
ANTHROPIC_API_KEY=
PEXELS_API_KEY=
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=
YOUTUBE_REFRESH_TOKEN=
```

---

## Приоритет реализации

1. `text_generator.py` — самое простое, проверить стиль
2. `image_fetcher.py` — Pexels API + дедупликация
3. `video_renderer.py` — FFmpeg сборка, самое сложное
4. `config_builder.py` — связывает всё вместе
5. `youtube_uploader.py` — в последнюю очередь

---

## Открытые вопросы (решить с пользователем)

- [ ] Язык канала — русский или английский?
- [ ] Движок который уже есть — что умеет, на чём написан?
- [ ] Анимация текста нужна или статичные слайды?
- [ ] Голосовой войсовер поверх музыки — нужен или только текст на экране?
- [ ] Где запускать — локально, VPS, или GitHub Actions?