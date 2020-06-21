from os import environ

import requests


class SpotifyAPIError(Exception):
    pass


def _get_token() -> str:
    # This two values are obtained following "Authorization Code Flow" in
    # https://developer.spotify.com/documentation/general/guides/authorization-guide/
    client_id = environ.get('SPOTIFY_CLIENT_B64')
    refresh_token = environ.get('SPOTIFY_REFRESH_TOKEN')
    body = dict(grant_type='refresh_token', refresh_token=refresh_token)
    headers = dict(Authorization=f'Basic {client_id}')
    response = requests.post(
        "https://accounts.spotify.com/api/token", data=body, headers=headers)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise SpotifyAPIError(response.json())


def get_tempo(track_id: str) -> float:
    """
    Get song tempo (BPM) from Spotify API.

    :param track_id: Song id in Spotify.
    :return: Song tempo.
    """
    token = _get_token()
    headers = dict(Authorization=f'Bearer {token}')
    endpoint = f'https://api.spotify.com/v1/audio-features/{track_id}'
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        return response.json().get('tempo')
    else:
        raise SpotifyAPIError(response.json())
