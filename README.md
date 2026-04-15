# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.
Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

In real apps, recommendations usually blend many signals—what you play, skip, save, and what similar users like—often with opaque models and huge catalogs. My simulation is deliberately small and transparent: I treat taste as stated preferences (genre, mood, energy, and whether I like acoustic tracks) and score each song with clear rules instead of learning from behavior at scale. My version will prioritize tracks that align with my favorite genre and mood, then refine the list using how close a song’s energy is to my target and whether its acousticness matches my likes_acoustic preference, so results stay explainable and easy to debug.

Each song is represented with:

Identity & display: id, title, artist
Categorical vibe: genre, mood
Numeric audio-style features (0–1 scale where applicable): energy, valence, danceability, acousticness
Tempo: tempo_bpm

The profile holds explicit preferences:

favorite_genre — preferred genre label (e.g. "pop")
favorite_mood — preferred mood label (e.g. "happy")
target_energy — preferred energy level on the same 0–1 style scale as songs
likes_acoustic — whether the user generally wants more acoustic-sounding tracks (True) or less (False)

The program have two parallel APIs: Recommender (OOP) and score_song / recommend_songs (functional). In both cases the idea is the same: build a scoring rule that adds weighted partial scores (and short “reason” strings for explanations), for example:

Genre: bonus when song.genre matches user.favorite_genre (often a large weight so style stays on-target).
Mood: bonus when song.mood matches user.favorite_mood.
Energy: closeness score so songs near user.target_energy beat songs that are only “high” or “low” in general.
Acousticness: small adjustment so high acousticness is rewarded when likes_acoustic is True, and penalized (or ignored) when it is False.

How do the program choose which songs to recommend?
Candidate set: all loaded songs (from the CSV via load_songs).
Per-song score: run your scoring rule for each song vs the user (dict prefs in main / UserProfile in tests).
Ranking rule: sort by total score descending and take the top k (e.g. k=5 in main, k=2 in tests).
Output: return ranked songs plus score and a short human-readable explanation built from the reasons you accumulated (as in main.py: song, score, because …).
That’s your ranking rule: “sort by score, then slice”—simple for this simulation; a fuller system might add diversity (avoid same artist back-to-back) on top of that ordering.


## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`,
---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

