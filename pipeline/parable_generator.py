#!/usr/bin/env python3
"""Generate parable batches for the shorts pipeline via Claude API."""

import json
import random
from datetime import datetime
from pathlib import Path

import anthropic

PARABLE_PROMPT = """
You write short parables for YouTube Shorts about language learning.

FORMAT:
- Exactly 8 screens
- Each screen: 2-4 lines maximum
- Label each screen: *Screen 1*, *Screen 2*, etc.
- Last screen is always the lesson — short, punchy, no more than 3 lines

STYLE:
- Simple, timeless language. No slang, no corporate words.
- A wise man, a student, a traveler, a craftsman — classic archetypes
- Build tension slowly. The twist or lesson lands on screen 7-8.
- Never explain the metaphor. Let it speak for itself.
- Warm but not soft. Direct but not harsh.

STRUCTURE that works:
- Screen 1-2: introduce the character and their question/problem
- Screen 3-4: the wise person responds — often with an unexpected action
- Screen 5-6: the tension or realization builds
- Screen 7: the turn — something shifts
- Screen 8: the lesson. 2-3 lines. No fluff.

TOPIC: language learning
- Fear of speaking
- Perfectionism vs progress
- The gap between studying and using
- Mistakes as the path, not the obstacle
- Finding your voice

LANGUAGE: English
TONE: timeless, calm, quietly powerful

Return only the parable. No titles. No explanations. No markdown except screen labels.
"""

PARABLE_TOPICS = [
    "speaking before you're ready",
    "the perfectionist who never speaks",
    "mistakes as the only real teacher",
    "the difference between knowing and using",
    "finding courage in a foreign country",
    "the student who studied for years but never talked",
    "two paths: perfection vs progress",
    "the moment everything clicks",
    "fear of being judged while speaking",
    "why children learn faster than adults",
    "the map is not the territory",
    "the sculptor who finds the voice inside the stone",
    "two students, two different paths to fluency",
    "the echo in the well",
    "the traveler who memorized every map but never left home",
]

# Maps topic keywords → Pexels search terms
TOPIC_KEYWORDS = {
    "traveler": ["misty road", "lone traveler"],
    "map": ["ancient path", "open road"],
    "sculptor": ["craftsman hands", "stone carving"],
    "student": ["open window light", "young person studying"],
    "well": ["calm water reflection", "stone well"],
    "perfectionist": ["morning desk", "open book"],
    "children": ["playground morning", "child learning"],
    "voice": ["microphone stage", "open window"],
    "courage": ["mountain path", "dawn light"],
    "fear": ["quiet room", "single candle"],
    "mistake": ["stepping stones", "trail path"],
    "fluency": ["conversation cafe", "people talking"],
}

DEFAULT_KEYWORDS = ["misty road", "quiet morning", "lone traveler"]


def _keywords_for_topic(topic: str) -> list[str]:
    for key, kws in TOPIC_KEYWORDS.items():
        if key in topic.lower():
            return kws
    return DEFAULT_KEYWORDS


def generate_parable(topic: str) -> str:
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=PARABLE_PROMPT,
        messages=[{"role": "user", "content": f"Write a new parable. Topic: {topic}"}],
    )
    return response.content[0].text


def parse_parable(raw_text: str) -> list[dict]:
    screens = []
    current_screen = None
    current_lines = []

    for line in raw_text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("*Screen"):
            if current_screen is not None:
                screens.append({
                    "screen": current_screen,
                    "text": "\n".join(current_lines).strip(),
                })
            current_screen = int(line.replace("*Screen", "").replace("*", "").strip())
            current_lines = []
        else:
            current_lines.append(line)

    if current_screen is not None:
        screens.append({
            "screen": current_screen,
            "text": "\n".join(current_lines).strip(),
        })

    return screens


def generate_parable_batch(
    count: int = 5,
    topics: list[str] = None,
    output_dir: str = "output/texts",
) -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    selected_topics = topics or random.sample(PARABLE_TOPICS, min(count, len(PARABLE_TOPICS)))

    parables = []
    for i, topic in enumerate(selected_topics):
        print(f"Generating parable {i + 1}/{len(selected_topics)}: {topic}")
        raw = generate_parable(topic)
        screens = parse_parable(raw)
        if len(screens) != 8:
            print(f"  Warning: got {len(screens)} screens instead of 8 — keeping anyway")
        parables.append({
            "id": f"parable_{i + 1:03d}",
            "topic": topic,
            "type": "parable",
            "mood": "calm",
            "keywords": _keywords_for_topic(topic),
            "screens": screens,
        })

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(output_dir) / f"parables_{timestamp}.json"
    output_path.write_text(json.dumps(parables, ensure_ascii=False, indent=2))

    print(f"\nSaved {len(parables)} parables to {output_path}")
    return str(output_path)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--output-dir", default="output/texts")
    args = parser.parse_args()
    generate_parable_batch(count=args.count, output_dir=args.output_dir)
