#!/usr/bin/env python3

from datetime import datetime
from utils import db_connection, db_cursor

import click
import httpx
import os


def write_artist(artist):
    if not artist["id"]:
        raise Exception("Spotify ID missing")
    sql = """
        INSERT INTO artists ( spotify_id, name )
        VALUES ( %(spotify_id)s, %(name)s )
        ON CONFLICT ( spotify_id ) DO
        UPDATE SET name = %(name)s, updated = %(updated)s
        WHERE artists.edited IS NULL
    """
    params = {
        "spotify_id": artist["id"],
        "name": artist["name"],
        "updated": datetime.now(),
    }
    db_cursor.execute(sql, params)
    db_connection.commit()
    return db_cursor.rowcount


def fetch_artists(artists, token) -> list:
    url = f"https://api.spotify.com/v1/artists"
    params = {"ids": ",".join(artists)}
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    print(f"fetching: {params}")
    response = httpx.get(url=url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()["artists"]


@click.command()
@click.option("-t", "--token", type=str, default=None, help="spotify api token")
@click.option("-a", "--artists", type=str, default=None, help="list of artist ids")
def main(token, artists):
    token = token or os.environ.get("SPOTIFY_TOKEN")
    if not token:
        raise Exception("No spotify token found.")

    artists = artists or (
        "2CIMQHirSU0MQqyYHq0eOx",
        "57dN52uHvrHOxijzpIgu3E",
        "1vCWHaC5f2uS3yhpwWbIA6",
        "4FVS2fGhv66N8QLEj77EEP",
    )
    for artist in fetch_artists(artists, token):
        if artist and artist.get("id"):
            write_artist(artist)
        else:
            print(f"Artist not found: {artist}")


if __name__ == "__main__":
    main()
