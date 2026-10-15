import math

import pytest

from src.recommender import Song, UserProfile, Recommender, score_song, recommend_songs

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genres=["pop"],
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genres=["pop"],
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


# --- Known gaps (⚠️) ---
# Each test below states the behavior we *want*. They are marked xfail because the
# current design does not do this yet. strict=True makes the test fail loudly once
# the gap is fixed, as a reminder to remove the xfail marker.

def make_song_dict(**overrides) -> dict:
    song = {
        "id": 1,
        "title": "Test Song",
        "artist": "Test Artist",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.5,
        "tempo_bpm": 100,
        "valence": 0.5,
        "acousticness": 0.5,
    }
    song.update(overrides)
    return song


@pytest.mark.xfail(strict=True, reason='"false" is a truthy string, so it is treated as likes_acoustic=True')
def test_likes_acoustic_rejects_non_bool_string():
    with pytest.raises((TypeError, ValueError)):
        UserProfile(
            favorite_genres=["pop"],
            favorite_mood="happy",
            target_energy=0.5,
            likes_acoustic="false",
        )


@pytest.mark.xfail(strict=True, reason="clamp() turns NaN into 1.0 instead of rejecting it")
def test_target_energy_rejects_nan():
    with pytest.raises(ValueError):
        UserProfile(
            favorite_genres=["pop"],
            favorite_mood="happy",
            target_energy=math.nan,
        )


@pytest.mark.xfail(strict=True, reason="only the user's target is clamped; out-of-range song energy goes negative")
def test_out_of_range_song_energy_never_scores_negative():
    user_prefs = {
        "favorite_genres": ["rock"],
        "favorite_mood": "sad",
        "target_energy": 0.0,
    }
    song = make_song_dict(energy=1.5)

    score, _ = score_song(user_prefs, song)
    assert score >= 0.0


@pytest.mark.xfail(strict=True, reason="scored[:-1] returns every song except the last")
def test_negative_k_is_rejected():
    user_prefs = {
        "favorite_genres": ["pop"],
        "favorite_mood": "happy",
        "target_energy": 0.5,
    }
    songs = [make_song_dict(id=1), make_song_dict(id=2), make_song_dict(id=3)]

    with pytest.raises(ValueError):
        recommend_songs(user_prefs, songs, k=-1)


@pytest.mark.xfail(strict=True, reason="songs are looked up by id, so duplicates collapse to the last one")
def test_recommend_keeps_distinct_songs_with_duplicate_ids():
    songs = [
        Song(id=1, title="First", artist="A", genre="pop", mood="happy",
             energy=0.8, tempo_bpm=120, valence=0.9, acousticness=0.2),
        Song(id=1, title="Second", artist="B", genre="lofi", mood="chill",
             energy=0.4, tempo_bpm=80, valence=0.6, acousticness=0.9),
    ]
    user = UserProfile(favorite_genres=["pop"], favorite_mood="happy", target_energy=0.8)

    results = Recommender(songs).recommend(user, k=2)
    assert [song.title for song in results] == ["First", "Second"]
