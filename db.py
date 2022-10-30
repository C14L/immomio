import logging
import psycopg2.extras

from datetime import datetime
from psycopg2.extensions import cursor as PsyCursor

from models import Artist

def get_unedited_artist_ids(csr: PsyCursor):
    sql = """
        SELECT spotify_id FROM artists
        WHERE edited IS NULL AND spotify_id IS NOT NULL
    """
    csr.execute(sql)
    return [x["spotify_id"] for x in csr.fetchall()]


def write_artist(csr: PsyCursor, artist: Artist):
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
    csr.execute(sql, params)
    return csr.rowcount
