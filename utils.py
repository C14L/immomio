from dotenv import load_dotenv, find_dotenv
from urllib.parse import urlparse

import os
import psycopg2
import psycopg2.extras


load_dotenv(find_dotenv())

db_auth = urlparse(os.environ.get("DB_URL"))
if not db_auth:
    raise Exception("No database connection string found in environment.")

db_connection = psycopg2.connect(
    dbname=db_auth.hostname,
    user=db_auth.username,
    password=db_auth.password,
    port=db_auth.port,
)

db_cursor = db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
