from common import utils


def test_playlist_parser():
    
    pid = utils.get_spotify_object_id(
        "https://open.spotify.com/playlist/37i9dQZF1DX2TRYkJECvfC?si=3050178e356d494b"
    )
    assert pid[2] == "37i9dQZF1DX2TRYkJECvfC"

    pid = utils.get_spotify_object_id(
        "37i9dQZF1DX2TRYkJECvfC"
    )
    assert pid[2] == "37i9dQZF1DX2TRYkJECvfC"

    pid = utils.get_spotify_object_id(
        "https://open.spotify.com/playlist/37i9dQZF1DX2TRYkJECvfC"
    )
    assert pid[2] == "37i9dQZF1DX2TRYkJECvfC"