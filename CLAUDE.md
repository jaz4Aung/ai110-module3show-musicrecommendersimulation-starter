# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run the simulation
python -m src.main

# Run tests
pytest

# Run a single test
pytest tests/test_recommender.py::test_recommend_returns_songs_sorted_by_score -v
```

## Architecture

This is a CodePath AI Module 3 project — a small music recommender simulation built to illustrate how recommenders turn stated preferences into scored rankings, with an emphasis on transparency and explainability.

### Data flow

`data/songs.csv` (10 songs) → `load_songs()` → list of dicts → `score_song()` per song → sorted by score → top-k returned with explanations.

### Two parallel APIs in `src/recommender.py`

**Functional API** (used by `src/main.py`):
- `load_songs(csv_path) -> List[Dict]` — reads CSV via pandas
- `score_song(user_prefs, song) -> Tuple[float, List[str]]` — scores one song; returns `(total_score, reason_strings)`
- `recommend_songs(user_prefs, songs, k=5) -> List[Tuple[Dict, float, str]]` — scores all songs, sorts descending, returns top k as `(song, score, explanation_string)`

**OOP API** (exercised by `tests/test_recommender.py`):
- `Song` dataclass — fields: `id, title, artist, genre, mood, energy, valence, danceability, acousticness, tempo_bpm`
- `UserProfile` dataclass — fields: `favorite_genre, favorite_mood, target_energy, likes_acoustic`
- `Recommender(songs: List[Song])` — wraps the catalog
  - `.recommend(user, k=5) -> List[Song]`
  - `.explain_recommendation(user, song) -> str`

### Scoring recipe (from README)

| Signal | Weight | Logic |
|---|---|---|
| Genre match | 2.0 | Exact match bonus |
| Mood match | medium | Exact match bonus |
| Energy closeness | medium | `1 - abs(song.energy - user.target_energy)` |
| Acousticness | small | Reward if `likes_acoustic`, ignore/penalize otherwise |

Each matched signal appends a human-readable reason string (e.g., `"matches favorite genre: pop"`). The explanation returned is a comma-joined string of all reason strings.

### Entry point

`src/main.py` hardcodes a sample user (`genre=pop, mood=happy, energy=0.8`), calls `recommend_songs()`, and prints results. Extend or swap the user profile here to demo different outputs.
