from dotenv import load_dotenv
from os import getenv

load_dotenv()

class Settings:
    database_url = getenv("DATABASE_URL")
    token = getenv("TOKEN")