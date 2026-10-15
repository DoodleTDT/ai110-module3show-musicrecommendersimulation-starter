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


# --- Edge cases ---

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


def test_likes_acoustic_rejects_non_bool_string():
    with pytest.raises(TypeError):
        UserProfile(
            favorite_genres=["pop"],
            favorite_mood="happy",
            target_energy=0.5,
            # Wrong type on purpose: this test checks that it gets rejected
            likes_acoustic="false",  # pyright: ignore[reportArgumentType]
        )


def test_target_energy_rejects_nan():
    with pytest.raises(ValueError):
        UserProfile(
            favorite_genres=["pop"],
            favorite_mood="happy",
            target_energy=math.nan,
        )


def test_out_of_range_song_energy_never_scores_negative():
    user_prefs = {
        "favorite_genres": ["rock"],
        "favorite_mood": "sad",
        "target_energy": 0.0,
    }
    song = make_song_dict(energy=1.5)

    score, _ = score_song(user_prefs, song)
    assert score >= 0.0


def test_negative_k_returns_empty_list_and_prints_message(capsys):
    user_prefs = {
        "favorite_genres": ["pop"],
        "favorite_mood": "happy",
        "target_energy": 0.5,
    }
    songs = [
        make_song_dict(id=1, title="One"),
        make_song_dict(id=2, title="Two"),
        make_song_dict(id=3, title="Three"),
    ]

    results = recommend_songs(user_prefs, songs, k=-1)
    assert results == []
    assert "positive number" in capsys.readouterr().out


@pytest.mark.parametrize("second_song", [
    # Same id, different song
    Song(id=1, title="Second", artist="B", genre="lofi", mood="chill",
         energy=0.4, tempo_bpm=80, valence=0.6, acousticness=0.9),
    # Different id, same title and artist (case and spacing ignored)
    Song(id=2, title=" first ", artist="a", genre="lofi", mood="chill",
         energy=0.4, tempo_bpm=80, valence=0.6, acousticness=0.9),
])
def test_recommender_rejects_duplicate_songs(second_song):
    songs = [
        Song(id=1, title="First", artist="A", genre="pop", mood="happy",
             energy=0.8, tempo_bpm=120, valence=0.9, acousticness=0.2),
        second_song,
    ]

    with pytest.raises(ValueError, match="duplicate"):
        Recommender(songs)
