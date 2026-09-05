# Parable Classic — Topics & Lessons

Scope: Zen/Buddhist-style parables with human archetypes (monk, student, traveler), `classic_NNN` IDs.

## Topic pool — pick one per parable, rotate across categories (no two consecutive parables from the same category)

**The lesson must be a reframe, not a command** — "you are not just learning words" not "go speak now."
**Specific detail over abstraction** — "she had friends in four countries" not "she succeeded."
**Screen 8 is the earliest the lesson can appear** — never before.
**Leave some things unresolved** — especially T12, T19, T20. Not every parable needs a happy ending.

### Identity & Change
| ID | Topic | Core tension | Avoid |
|----|-------|-------------|-------|
| T01 | Language changes personality — you become a different person in a new language | Who is the "real" you? | Don't moralize. Let the character decide. |
| T02 | Losing your accent as losing yourself — when fluency costs too much | Belonging vs. achievement | Don't resolve it neatly. Leave it open. |
| T03 | The moment you first dream in a foreign language | Surprise, not effort | Don't make it about hard work. It just happened. |
| T04 | A bilingual child who switches between two versions of themselves | Duality as strength | Don't make it a problem to solve. |

### The Middle of the Road
| ID | Topic | Core tension | Avoid |
|----|-------|-------------|-------|
| T05 | The plateau — progress stops and it feels like nothing is working | Persistence without reward | Don't promise it gets better. Sit in it. |
| T06 | A person who has studied for 10 years and still calls themselves a beginner | Self-perception vs. reality | Don't tell them they're wrong. Ask why. |
| T07 | The day motivation disappeared — and what happened next | Discipline vs. feeling | Don't replace motivation with discipline speech. |
| T08 | Exhaustion from the language — wanting to quit but being too far in | Sunk cost, not failure | Don't make quitting wrong. Make continuing honest. |

### Connection & People
| ID | Topic | Core tension | Avoid |
|----|-------|-------------|-------|
| T09 | A word that cannot be translated — and what it reveals about the people who use it | Language as worldview | Don't explain the word. Let it stay mysterious. |
| T10 | Speaking to a grandparent in their language for the first time | Regret and arrival | Don't sentimentalize. Keep it spare. |
| T11 | A person who learned a language for one specific person | Love as motivation | Don't judge the reason. Honor it. |
| T12 | Losing your native language after years abroad | Grief, not failure | Don't offer a solution. This is a real loss. |

### Time & Patience
| ID | Topic | Core tension | Avoid |
|----|-------|-------------|-------|
| T13 | A tree that grows slowly — on long journeys with no visible results | Faith without proof | Don't rush to the payoff. The slowness is the point. |
| T14 | An old person who starts learning a language at 70 — and why | It's never too late, but reframed | Don't make it inspirational. Make it quiet and true. |
| T15 | A person who quit and came back 5 years later | Return without shame | Don't make quitting a mistake. Make returning a choice. |

### Fear & Shame
| ID | Topic | Core tension | Avoid |
|----|-------|-------------|-------|
| T16 | The shame of an accent — and why an accent is not an error | Identity in sound | Don't fix the shame. Reframe what it means. |
| T17 | A person who stayed silent for a year before speaking a word aloud | Fear as information | Don't rush them. The silence means something. |
| T18 | Being laughed at for a mistake — who laughs and why it doesn't matter | Embarrassment vs. growth | Don't minimize the laugh. Redirect its meaning. |

### Provocation
| ID | Topic | Core tension | Avoid |
|----|-------|-------------|-------|
| T19 | The language you don't need to learn — on choice and honesty with yourself | Permission to stop | Don't make this negative. Make it liberating. |
| T20 | A person who speaks five languages and feels at home in none | Mastery without belonging | Don't resolve this. End in the question. |

## Used final lessons (avoid repeating, going forward under classic_ IDs)

Historical note: the original `parable_001–005` (legacy IDs, pre-restructure) all landed on variations of "act before you're ready":
- A language lived in is never perfect. A language studied in is never alive.
- He had forgotten most of the maps. But he knew every road by heart.
- Stop adding. Start removing the fear.
- Fluency is not the absence of mistakes. It is the decision to speak before you are ready.
- The language only teaches you when you speak into it. Silence has no echo.

New entries (append after each generated classic parable):

- classic_023: "The woman had already gone." / "The student had needed to hear it from the world."
- classic_024: "Three words and a willing face is more than three hundred words and a closed one."
- classic_025: "He was a stranger. Strangers are kinder mirrors than teachers."
- classic_026: "She had been running from something the other person didn't mind carrying."
- classic_027: "By today you were doing it yourself."
- classic_028: "You spent two years filling a jar. You had not learned to pour from it."
- classic_029: "The teacher's mistakes had been the real lesson."
- classic_030: "It was a moment. That was enough."
- classic_031: "The young man was still thinking about whether it was too late for him."
- classic_032: "That is a very quiet place to live in another language."
- classic_033: "He had been somewhere and we had only been thinking."
- classic_034: "The view from inside was nothing like the view from the window."
- classic_035: "He understood what she didn't say."
- classic_036: "The language had been waiting. The way all things wait that were once truly learned."
- classic_037: "The silence had held them both. Neither of them had fallen."
- classic_038: "She had not noticed until now that expertise can make you quiet."
- classic_039: "He was only one sentence behind. The year after that he stopped counting."
- classic_040: "She had finally understood what she had been studying."

## Voice selection

Rotate across all four voices — don't use the same one twice in a row.

| Voice | Character | Best for |
|-------|-----------|----------|
| `elder` | Contemplative, measured | Wisdom parables, slow reveals, introspective tone |
| `abbot` | Authoritative, gravelly | Tension, corporate pressure, confrontation scenes |
| `thomas` | Measured, neutral | Tender moments, female protagonists, quiet endings |
| `oliver` | Warm, classic | Timeless archetypes, gentle humor, human connection |

Override per render: `PREMISS_VOICE=abbot python3 main.py`
