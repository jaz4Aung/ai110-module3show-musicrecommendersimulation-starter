from typing import List, Dict, Tuple
from dataclasses import dataclass
import pandas as pd


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> float:
        """Returns a numeric score for one song against a UserProfile using genre, mood, energy, and acousticness signals."""
        s = 0.0
        if song.genre == user.favorite_genre:
            s += 2.0
        if song.mood == user.favorite_mood:
            s += 1.0
        s += 1.0 - abs(song.energy - user.target_energy)
        if song.acousticness >= 0.6:
            s += 0.5 if user.likes_acoustic else -0.5
        return s

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top-k Song objects ranked by descending score for the given UserProfile."""
        return sorted(self.songs, key=lambda song: self._score(user, song), reverse=True)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a comma-joined string of human-readable reasons why a song was recommended."""
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append(f"genre match: {song.genre} (+2.0)")
        if song.mood == user.favorite_mood:
            reasons.append(f"mood match: {song.mood} (+1.0)")
        energy_score = 1.0 - abs(song.energy - user.target_energy)
        reasons.append(f"energy closeness: {energy_score:.2f}")
        if song.acousticness >= 0.6:
            if user.likes_acoustic:
                reasons.append("acoustic texture: liked (+0.5)")
            else:
                reasons.append("acoustic texture: disliked (-0.5)")
        return ", ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file using pandas.
    Numeric columns are cast to float; id is cast to int.
    Required by src/main.py
    """
    df = pd.read_csv(csv_path)

    float_cols = ["energy", "tempo_bpm", "valence", "danceability", "acousticness"]
    for col in float_cols:
        df[col] = df[col].astype(float)
    df["id"] = df["id"].astype(int)

    return df.to_dict(orient="records")


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.

    Algorithm recipe (max 6.0 points):
      +2.0  genre exact match
      +1.0  mood exact match
      +1.0  energy closeness   — 1 - |song.energy - target_energy|
      +0.5  valence closeness  — 0.5 * (1 - |song.valence - target_valence|)
      +0.5  danceability       — 0.5 * (1 - |song.danceability - target_danceability|)
      ±0.5  acousticness fit   — +0.5 if likes_acoustic and acousticness >= 0.6
                                 -0.5 if not likes_acoustic and acousticness >= 0.6
      +0.5  tempo closeness    — 0.5 * max(0, 1 - |bpm - target| / 80)

    Returns (total_score, reason_strings).
    """
    score = 0.0
    reasons: List[str] = []

    # Genre match
    if song.get("genre") == user_prefs.get("genre"):
        score += 2.0
        reasons.append(f"genre match: {song['genre']} (+2.0)")

    # Mood match
    if song.get("mood") == user_prefs.get("mood"):
        score += 1.0
        reasons.append(f"mood match: {song['mood']} (+1.0)")

    # Energy closeness (always applied when target_energy is present)
    if "target_energy" in user_prefs:
        energy_score = 1.0 - abs(song["energy"] - user_prefs["target_energy"])
        score += energy_score
        reasons.append(f"energy closeness: {energy_score:.2f}")

    # Valence closeness
    if "target_valence" in user_prefs:
        valence_score = 0.5 * (1.0 - abs(song["valence"] - user_prefs["target_valence"]))
        score += valence_score
        reasons.append(f"valence closeness: {valence_score:.2f}")

    # Danceability closeness
    if "target_danceability" in user_prefs:
        dance_score = 0.5 * (1.0 - abs(song["danceability"] - user_prefs["target_danceability"]))
        score += dance_score
        reasons.append(f"danceability closeness: {dance_score:.2f}")

    # Acousticness fit
    if "likes_acoustic" in user_prefs:
        if song["acousticness"] >= 0.6:
            if user_prefs["likes_acoustic"]:
                score += 0.5
                reasons.append("acoustic texture: liked (+0.5)")
            else:
                score -= 0.5
                reasons.append("acoustic texture: disliked (-0.5)")

    # Tempo closeness
    if "target_tempo_bpm" in user_prefs:
        tempo_score = 0.5 * max(0.0, 1.0 - abs(song["tempo_bpm"] - user_prefs["target_tempo_bpm"]) / 80.0)
        score += tempo_score
        reasons.append(f"tempo closeness: {tempo_score:.2f}")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Scores every song, sorts descending, returns top k as (song, score, explanation).
    Required by src/main.py

    Why sorted() instead of list.sort():
      - list.sort() mutates the original list in place and returns None.
      - sorted() returns a brand-new sorted list, leaving the input untouched.
      Since we need to slice the result anyway ([:k]) and callers may reuse
      the original songs list, sorted() is the more Pythonic choice here.
    """
    scored = [
        (song, total, ", ".join(reasons))
        for song in songs
        for total, reasons in [score_song(user_prefs, song)]
    ]
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
