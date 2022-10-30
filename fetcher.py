import httpx

from typing import List


def fetch_artists(artist_ids: List[str], token: str) -> list:
    url = f"https://api.spotify.com/v1/artists"
    params = {"ids": ",".join(artist_ids)}
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    response = httpx.get(url=url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()["artists"]
