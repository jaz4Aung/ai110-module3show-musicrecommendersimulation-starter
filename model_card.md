# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Goal / Task

VibeFinder suggests 5 songs from a 20-song catalog that best match a user's stated taste
profile. It is built for classroom exploration of how recommender systems work — not for
real users or production use.

The system assumes the user can describe their taste with explicit labels (genre, mood)
and numeric targets (energy level, tempo, etc.). It does not learn from listening history,
skips, or saves.

**Intended use:** Learning how scoring-based recommenders work. Experimenting with
weights, profiles, and edge cases to understand bias and explainability.

**Non-intended use:** This system should not be used to make real music recommendations
for real listeners. It has a 20-song catalog, no personalisation, no content filtering,
and no awareness of context (time of day, activity, mood changes). It should not be
deployed in any product, embedded in a streaming app, or used to drive user engagement.
Using it as a real recommender would produce repetitive, narrow results and could
reinforce existing taste rather than helping users discover new music.

---

## 3. How the Model Works

Think of it as a judge scoring a talent show. Every song in the catalog has to perform
in front of the judge (your taste profile), and the judge awards points based on how well
the song matches each preference.

The judge gives the biggest reward for style: if a song is in your favourite genre, it
gets an automatic +2 points out of a possible 6. If it also matches your preferred mood,
it earns another +1. After that, the judge scores how close the song feels to your
preferences on energy, brightness (valence), groove (danceability), acoustic texture,
and tempo — each worth smaller amounts. All the points are added up, the songs are
sorted from highest to lowest, and the top five go on your playlist.

Every recommendation comes with a plain-English explanation of exactly which points were
awarded, so you can always see why a song made the list.

---

## 4. Data

The catalog contains 20 songs stored in `data/songs.csv`. The original starter file had
10 songs; 10 more were added to improve diversity.

Genres represented: pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, r&b,
classical, country, electronic, reggae, metal, folk, blues, k-pop.

Moods represented: happy, chill, intense, relaxed, moody, focused, confident, romantic,
peaceful, nostalgic, euphoric, uplifting, angry, melancholic, sad, upbeat.

Each genre and mood appears exactly once (except lofi which has three songs and pop which
has two). The numeric features (energy, valence, danceability, acousticness, tempo) were
chosen to reflect realistic audio characteristics for each genre.

Whose taste does this data mostly reflect? The catalog skews toward English-language
Western genres. There is no representation of genres like Afrobeats, Latin, or J-pop.
All songs are fictional with invented artist names.

---

## 5. Strengths

- **Clear niche users are served well.** The lofi profile returned a near-perfect score
  (5.96/6.00) because the catalog has three lofi songs that closely match the target
  numeric features. The rock profile similarly topped out at 5.47. When the genre exists
  in the catalog and the numeric features match, results feel accurate and intuitive.

- **Explainability is a genuine strength.** Every result includes a reason string showing
  exactly which signals fired and for how many points. A non-programmer can read
  "genre match: pop (+2.0), mood match: happy (+1.0)" and immediately understand why
  Sunrise City was ranked first.

- **Adversarial profiles do not crash or behave randomly.** Even contradictory input
  (high energy + sad mood, or acoustic lover wanting metal) produces a ranked list with
  consistent logic — the genre+mood match still wins, which is a reasonable fallback.

---

## 6. Limitations and Bias

**Genre dominance.** The genre weight (+2.0) is 33% of the maximum possible score.
This means a song in the right genre always has a large head start, even if every other
numeric feature is a poor match. In the rock experiment, Storm Runner scored 5.47 while
second place (Gym Hero, wrong genre) scored only 3.09 — a 2.38-point gap created
entirely by the genre bonus. A great song in a neighbouring genre like "indie rock" would
score zero on genre and never break into the top results.

**Exact-match brittleness.** Genre and mood are compared as exact strings. "indie pop"
and "pop" are treated as completely different, even though they are closely related. A
user who likes pop will never be recommended Rooftop Lights (indie pop) through the genre
signal — only through numeric closeness. Real systems use vector embeddings to capture
genre similarity.

**Acousticness cliff.** The ±0.5 acousticness rule only fires for songs with
`acousticness ≥ 0.6`. A song at 0.59 is treated identically to a fully electronic one.
This creates an invisible threshold that users cannot see or control.

**Filter bubble for under-represented genres.** Genres like jazz, classical, and blues
each appear only once. A jazz fan gets one correct genre match and then falls into
numeric-only ranking for the remaining four results. The recommendations feel thin
compared to a lofi fan who has three genre matches to choose from.

**Cold-start — no learning.** The profile is entirely hand-coded. The system has no way
to improve based on what the user actually plays, skips, or saves. Every run produces
identical results for the same profile.

---

## 7. Evaluation

Five user profiles were tested: three realistic and two adversarial.

**Profile 1 — High-Energy Pop:** Sunrise City topped the list at 5.44 with both genre
and mood matching. Gym Hero came second (pop genre, but mood was "intense" not "happy").
This felt correct — Sunrise City is a much better match for someone who wants happy pop.
Surprising: Neon Runway (k-pop) and Crown Season (hip-hop) appeared at #4 and #5
because their numeric features are close even though the genre is wrong. Without the
genre weight, they would rank higher.

**Profile 2 — Chill Lofi:** Near-perfect results. Three lofi songs occupied the top 3,
with Midnight Coding scoring 5.96/6.00. This is the profile the system handles best
because the catalog happens to have three lofi songs with well-matched numeric features.

**Profile 3 — Deep Intense Rock:** Storm Runner was a clear #1 (only rock song). The
drop to #2 was dramatic — from 5.47 to 3.09 — because there is only one rock song. The
remaining slots filled with high-energy songs from other genres. This exposed the
single-song-per-genre problem.

**Edge Case 1 — High Energy + Sad Mood:** The system found the one blues/sad song
(3am Confession, 5.42) and put it first, even though its energy (0.44) is far from the
target (0.9). The genre+mood bonus (3.0 points combined) overrode the large energy
penalty. This shows the system prioritises style over feel.

**Weight-shift experiment (genre 2.0→1.0, energy 1.0→2.0):** The pop profile's ranking
shifted noticeably. Rooftop Lights jumped from #3 to #2 (its energy of 0.76 is closer to
the 0.8 target than Gym Hero's 0.93). Neon Runway and Crown Season moved from ~2.2 to
~3.2, nearly matching Gym Hero. Reducing the genre weight makes the system more
energy-driven and less style-driven — results feel more "vibe-based" and less
"genre-loyal."

---

## 8. Future Work

- **Fuzzy genre matching.** Use genre similarity groups (e.g. pop ≈ indie pop ≈ k-pop)
  so related genres earn partial credit instead of zero.
- **Larger, balanced catalog.** Add 3–5 songs per genre so no single genre runs out of
  candidates after the first match.
- **User feedback loop.** Track which recommendations were accepted or skipped and
  adjust weights accordingly over time.
- **Diversity filter.** Prevent the same artist from appearing more than once in the
  top-k results (LoRoom appears twice in the lofi results).
- **Configurable weights.** Let the user tune genre vs. energy importance through a
  simple slider, rather than hard-coding weights in the source.

---

## 9. Personal Reflection

**Biggest learning moment:** The weight-shift experiment. Halving the genre weight from
2.0 to 1.0 completely reshuffled the #2 and #3 spots, and non-pop songs jumped nearly
a full point. That made it obvious that a recommender's "personality" lives in its
weights, not its data. The same 20 songs produce a style-loyal system or a vibe-driven
system just by changing one number.

**Using AI tools:** AI helped most with the parts that are tedious but not hard —
generating the extra 10 songs in valid CSV format, suggesting the Mermaid flowchart
syntax, and drafting the plain-language explanations in this model card. The parts that
needed double-checking were anything involving scoring math. The AI sometimes suggested
reason strings that didn't match the actual formula, so I always verified the output
against what `score_song` actually computed before accepting it.

**What surprised me about simple algorithms:** The output genuinely feels like a
recommendation even though it is just addition and sorting. When the lofi profile
returns Midnight Coding at 5.96/6.00 with the reason "genre match, mood match, energy
closeness: 0.98, acoustic texture: liked," it reads like something a knowledgeable
friend would say. The transparency is what makes it feel trustworthy — you can see
exactly why each song was chosen, which is something most real recommenders deliberately
hide.

**What I would try next:** The most meaningful improvement would be fuzzy genre
matching — grouping "pop," "indie pop," and "k-pop" so they earn partial credit for
each other instead of zero. Right now the system treats genre as a hard wall. Making it
a soft boundary would let the catalog's diversity actually show up in the results,
especially for users whose favourite genre has only one song.
