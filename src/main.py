"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # --- User Taste Profile ---
    # Critique: The original 3-key profile {genre, mood, energy} is too narrow.
    #
    # Problem 1 — Energy alone does not fully separate "intense rock" from "electronic":
    #   Storm Runner (rock, energy=0.91) and Laser Horizon (electronic, energy=0.95)
    #   both score nearly identically on energy. Without acousticness or genre weight,
    #   a rock fan and an EDM fan get the same top result.
    #
    # Problem 2 — Mood collisions: "chill lofi" and "ambient" both map to mood=chill.
    #   A profile with only mood="chill" cannot tell them apart. Adding target_valence
    #   breaks the tie — lofi tends toward 0.56–0.60, ambient toward 0.65.
    #
    # Problem 3 — No texture signal: two songs can share genre+mood+energy but differ
    #   wildly in feel (acoustic guitar vs synth pad). likes_acoustic captures this.
    #
    # Solution — add valence, danceability, acousticness, and tempo targets so every
    #   dimension of the song vector contributes to the final score.

    user_prefs = {
        "genre": "pop",           # primary genre preference (weight 2.0 in scorer)
        "mood": "happy",          # target emotional tone
        "target_energy": 0.8,     # 0.0 = very calm, 1.0 = maximum intensity
        "likes_acoustic": False,  # False → penalise high acousticness songs
        "target_valence": 0.80,   # 0.0 = dark/negative, 1.0 = bright/positive
        "target_danceability": 0.80,  # rewards groovy, rhythmic tracks
        "target_tempo_bpm": 120,  # separates metal (168) from hip-hop (95) at equal energy
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    # --- Formatted output ---
    width = 54
    bar = "=" * width

    print()
    print(bar)
    print(f"  Music Recommender  |  {user_prefs['genre'].upper()} / {user_prefs['mood'].upper()}")
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
        # Wrap reasons onto separate indented lines for readability
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
        print(f"  {'-' * (width - 2)}")


if __name__ == "__main__":
    main()
