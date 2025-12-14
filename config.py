import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load .env file
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise EnvironmentError("Missing MONGO_URI in environment")

client = MongoClient(MONGO_URI)
db = client.music_app
users = db.users
