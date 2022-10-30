import os
import psycopg2

from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from fastapi import Depends, FastAPI
from fastapi.responses import RedirectResponse
from fastapi_utils.tasks import repeat_every
from psycopg2.extensions import connection as PsyConnection
from psycopg2.extensions import cursor as PsyCursor
from typing import List
from urllib.parse import urlparse

from db import get_unedited_artist_ids, write_artist
from fetcher import fetch_artists
from models import Artist, WritableArtist


load_dotenv(find_dotenv())

FREQUENCY = 60  # sec

app = FastAPI()

_db_conn: PsyConnection


@app.on_event("startup")
def connect_db():
    global _db_conn
    print("Opening DB connection")

    db_auth = urlparse(os.environ.get("DB_URL"))
    if not db_auth:
        raise Exception("No database connection string found in environment.")

    _db_conn = psycopg2.connect(
        dbname=db_auth.path[1:],
        user=db_auth.username,
        password=db_auth.password,
        port=db_auth.port,
    )
    _db_conn.set_session(autocommit=True)


@app.on_event("shutdown")
def disconnect_db():
    global _db_conn
    _db_conn.close()


def get_db_csr() -> PsyCursor:
    return _db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


@app.on_event("startup")
@repeat_every(seconds=FREQUENCY, raise_exceptions=True, wait_first=True)
def fetch_artists_task(csr=Depends(get_db_csr)):
    print("This is fetch_artists_task() task")

    token = os.environ.get("SPOTIFY_TOKEN")
    if not token:
        raise Exception("No spotify token found.")

    csr = csr.dependency()
    artist_ids = get_unedited_artist_ids(csr)
    print(f"Found {len(artist_ids)} artists to update")

    for artist in fetch_artists(artist_ids, token):
        if artist and artist.get("id"):
            print(f"Updating ID {artist['id']}...")
            write_artist(csr, artist)
        else:
            print("Artist not found: ", artist)


@app.get("/")
async def root():
    return RedirectResponse("/artists/", status_code=303)


@app.get("/artists/", response_model=List[Artist])
async def artist_list(csr=Depends(get_db_csr)):
    csr.execute("SELECT * FROM artists ORDER BY id ASC")
    return csr.fetchall()


@app.post("/artists/", response_model=int)
async def artist_create(artist: WritableArtist, csr=Depends(get_db_csr)):
    sql = "INSERT INTO artists (name, edited) VALUES (%(name)s, %(edited)s)"
    params = {"name": artist.name, "edited": datetime.now()}
    csr.execute(sql, params)
    return csr.rowcount


@app.get("/artists/{artist_id}", response_model=Artist)
async def artist_read(artist_id: int, csr=Depends(get_db_csr)):
    sql = "SELECT * FROM artists WHERE id = %(id)s"
    params = {"id": artist_id}
    csr.execute(sql, params)
    return csr.fetchone()


@app.put("/artists/{artist_id}", response_model=int)
async def artist_update(
    artist_id: int, artist: WritableArtist, csr=Depends(get_db_csr)
):
    sql = "UPDATE artists SET name = %(name)s, edited = %(edited)s WHERE id = %(id)s"
    params = {"id": artist_id, "edited": datetime.now(), "name": artist.name}
    csr.execute(sql, params)
    return csr.rowcount


@app.delete("/artists/{artist_id}", response_model=int)
async def artist_delete(artist_id: int, csr=Depends(get_db_csr)):
    sql = "DELETE FROM artists WHERE id = %(id)s"
    params = {"id": artist_id}
    csr.execute(sql, params)
    return csr.rowcount
