from pony.orm import Database
import os
from dotenv import load_dotenv

load_dotenv()

db = Database()
db.bind(
    provider="postgres",
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "postgres"),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    database=os.getenv("POSTGRES_DB", "farmdb"),
    port=os.getenv("POSTGRES_PORT", "5432")
)
