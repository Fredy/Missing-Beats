from os import environ

import requests


class SpotifyAPIError(Exception):
    pass


def get_tempo(track_id: str) -> float:
    """
    Get song tempo (BPM) from Spotify API.

    :param track_id: Song id in Spotify.
    :return: Song tempo.
    """
    token = environ.get('SPOTIFY_TOKEN')
    headers = dict(Authorization=f'Bearer {token}')
    endpoint = f'https://api.spotify.com/v1/audio-features/{track_id}'
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        return response.json().get('tempo')
    else:
        raise SpotifyAPIError(response.json())
