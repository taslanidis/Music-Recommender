import pytest

from spotify_connectors.spotify_web_api import SpotifyWebAPI


@pytest.fixture
def spotify_web_api():
    instance = SpotifyWebAPI()
    yield instance


def test_get_playlist_tracks(spotify_web_api: SpotifyWebAPI):
    result = spotify_web_api.get_playlist_tracks(
        playlist_id="https://open.spotify.com/playlist/4eM0vCIishUmSAzFvouHUK?si=feee37bc977b4b02"
    )
    assert(len(result) > 5)
    assert(len(result[0].artists) > 0)


def test_get_track(spotify_web_api: SpotifyWebAPI):
    track = spotify_web_api.get_track(
        track_id="https://open.spotify.com/track/7LVHVU3tWfcxj5aiPFEW4Q?si=33eb982021b54169"
    )
    assert(track.name == "Fix You")
    assert(len(track.artists) > 0)


def test_get_enhanced_track(spotify_web_api: SpotifyWebAPI):
    track = spotify_web_api.get_enhanced_track(
        track_id="https://open.spotify.com/track/7LVHVU3tWfcxj5aiPFEW4Q?si=33eb982021b54169"
    )
    assert(track.name == "Fix You")
    assert(len(track.artists) > 0)
    assert(track.audio_features.danceability > 0)


def test_enhance_tracks_with_artist_information(spotify_web_api: SpotifyWebAPI):
    result = spotify_web_api.get_playlist_tracks(
        playlist_id="https://open.spotify.com/playlist/4eM0vCIishUmSAzFvouHUK?si=feee37bc977b4b02"
    )

    enhanced_tracks = spotify_web_api.enhance_tracks_with_artist_information(
        tracks=result[0:1]
    )
    assert(enhanced_tracks[0].name == "Fix You")
    assert(len(enhanced_tracks[0].artists) > 0)
    assert(len(enhanced_tracks[0].artists[0].genres) > 0)
    assert(enhanced_tracks[0].artists[0].popularity > 0)
