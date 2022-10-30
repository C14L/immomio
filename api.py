from datetime import datetime
from fastapi import FastAPI
from models import Artist
from utils import db_connection, db_cursor

app = FastAPI()


@app.get("/ping")
async def ping():
    return "pong"


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.get("/artists/")
async def artist_list():
    db_cursor.execute("SELECT * FROM artists")
    return db_cursor.fetchall()


@app.post("/artists/")
async def artist_create(artist: Artist):
    sql = "INSERT INTO artists (name, edited) VALUES (%(name)s, %(edited)s)"
    params = {"name": artist.name, "edited": datetime.now()}
    db_cursor.execute(sql, params)
    return db_cursor.rowcount


@app.get("/artists/{id_}")
async def artist_read(id_: str):
    sql = "SELECT * FROM artists WHERE id = %(id)s"
    params = {"id": id_}
    db_cursor.execute(sql, params)
    return db_cursor.fetchone()


@app.put("/artists/{id_}")
async def artist_update(id_: str):
    sql = "UPDATE artists SET name = %(name) WHERE id = %(id)s"
    params = {"id": id_}
    db_cursor.execute(sql, params)
    return db_cursor.rowcount


@app.delete("/artists/{id_}")
async def artist_delete(id_: str):
    sql = "DELETE FROM artists WHERE id = %(id)s"
    params = {"id": id_}
    db_cursor.execute(sql, params)
    return db_cursor.rowcount
