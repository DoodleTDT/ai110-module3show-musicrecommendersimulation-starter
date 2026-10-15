# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

In this small music recommendation system, it will prioritize User preferences against genres (and genres associated), mood, energy, and acoustics through a weighted scale, ranking the top scored songs in a currated list. This model will assume the user does not know the songs and artists in the database, so the user will not be reccomended songs based on those two categories like other music recommenders.

---

## How The System Works

Each `Song` has four things used in the system: genre, mood, energy, and acousticness. Title and artist is for display only.

A `UserProfile` stores: 
- a list of favorite genres of 1 to 3 songs
- a favorite mood
- a preferred amount of energy from 0 to 1
- a toggle for if user likes acoustics or not

The scoring rule for each song goes as follows:

1| Favorite genres are given the highest weight of 4.0 points. There are no extra rankings between a list of genres Genres that are an extension of a favorite are also weighed the same. 
- Example: Favorite genre of `rock` == `rock` and `indie rock`
- Example: Favorite genre of `indie rock` == `indie rock` (since it is a specific genre)

2| Mood has a weighted score of 2.0 points. If the mood matches the one in the favorites, it is awarded those points.

3| Energy is also weighted at 2.0 points. If the energy is closer to the target energy in `UserProfile`, it is given more points.
- Example: Target energy of 0.20 will award more points to songs with 0.12 energy compared to songs with 0.78 energy

4| Acousticness is the lowest weight of 1.0 point, and is an optional preference. If the user likes acoustics, then each song will be scored higher the more acoustics it has. Same goes for if the user does not want acoustics. Songs with less will be scored higher in that category. If acoustics are left out by the user, than it will not be considered during the final score.

Every song will go through these scoring rules, and the songs with the highest scores will be added to the recommendation list first.

---

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

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

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



