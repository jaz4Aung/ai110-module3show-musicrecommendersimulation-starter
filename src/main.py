"""
Command line runner for the Music Recommender Simulation.

Runs five user profiles — three realistic and two adversarial edge cases —
to stress-test the scoring logic and reveal any unexpected behaviour.
"""

from src.recommender import load_songs, recommend_songs


WIDTH = 54


def print_recommendations(label: str, user_prefs: dict, recommendations: list) -> None:
    """Prints a formatted results block for one user profile."""
    bar = "=" * WIDTH
    print()
    print(bar)
    print(f"  {label}")
    print(f"  Profile: {user_prefs['genre'].upper()} / {user_prefs['mood'].upper()}")
    print(bar)
    print(f"  Genre : {user_prefs['genre']:<10}  Mood    : {user_prefs['mood']}")
    print(f"  Energy: {user_prefs['target_energy']:<10}  Acoustic: {'Yes' if user_prefs['likes_acoustic'] else 'No'}")
    print(f"  Valence: {user_prefs['target_valence']:<9}  Dance   : {user_prefs['target_danceability']}")
    print(f"  Tempo : {user_prefs['target_tempo_bpm']} BPM")
    print(bar)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print()
        print(f"  #{rank}  {song['title']}  ({song['artist']})")
        print(f"       Score  : {score:.2f} / 6.00")
        reasons = explanation.split(", ")
        reason_lines = []
        line = ""
        for r in reasons:
            candidate = f"{line}, {r}" if line else r
            if len(candidate) > 44:
                reason_lines.append(line)
                line = r
            else:
                line = candidate
        if line:
            reason_lines.append(line)
        indent = "       Why    : "
        cont   = "               "
        for i, rl in enumerate(reason_lines):
            print(f"{indent if i == 0 else cont}{rl}")
        print(f"  {'-' * (WIDTH - 2)}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    profiles = [
        # --- Normal profiles ---
        (
            "Profile 1: High-Energy Pop",
            {
                "genre": "pop",
                "mood": "happy",
                "target_energy": 0.8,
                "likes_acoustic": False,
                "target_valence": 0.80,
                "target_danceability": 0.80,
                "target_tempo_bpm": 120,
            },
        ),
        (
            "Profile 2: Chill Lofi",
            {
                "genre": "lofi",
                "mood": "chill",
                "target_energy": 0.4,
                "likes_acoustic": True,
                "target_valence": 0.58,
                "target_danceability": 0.60,
                "target_tempo_bpm": 78,
            },
        ),
        (
            "Profile 3: Deep Intense Rock",
            {
                "genre": "rock",
                "mood": "intense",
                "target_energy": 0.92,
                "likes_acoustic": False,
                "target_valence": 0.45,
                "target_danceability": 0.65,
                "target_tempo_bpm": 152,
            },
        ),
        # --- Adversarial / edge-case profiles ---
        (
            "Edge Case 1: High Energy + Sad Mood",
            # Conflicting signals: energy=0.9 pulls toward metal/electronic,
            # but mood=sad only exists in blues (low energy). The scorer has
            # to choose — watch which signal wins.
            {
                "genre": "blues",
                "mood": "sad",
                "target_energy": 0.9,
                "likes_acoustic": True,
                "target_valence": 0.25,
                "target_danceability": 0.45,
                "target_tempo_bpm": 80,
            },
        ),
        (
            "Edge Case 2: Acoustic Lover Wants Metal",
            # Contradictory: likes_acoustic=True but genre=metal.
            # No metal song has acousticness >= 0.6, so the acoustic
            # bonus never fires — reveals the acousticness cliff bias.
            {
                "genre": "metal",
                "mood": "angry",
                "target_energy": 0.97,
                "likes_acoustic": True,
                "target_valence": 0.20,
                "target_danceability": 0.45,
                "target_tempo_bpm": 168,
            },
        ),
    ]

    for label, user_prefs in profiles:
        recs = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(label, user_prefs, recs)


if __name__ == "__main__":
    main()
