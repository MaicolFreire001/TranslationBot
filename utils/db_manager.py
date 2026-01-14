import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["TranslationConfig"]
collection = db["server_configs"]

def get_config(guild_id):
    config = collection.find_one({"_id": str(guild_id)})
    if not config:
        default_config = {
            "_id": str(guild_id),
            "lang": "es", 
            "auto": False
        }
        collection.insert_one(default_config)
        return default_config
    return config

def update_config(guild_id, **kwargs):
    collection.update_one(
        {"_id": str(guild_id)},
        {"$set": kwargs},
        upsert=True
    )

def init_db():
    try:
        client.admin.command('ping')
        print("✅ Conectado a MongoDB Atlas", flush=True)
    except Exception as e:
        print(f"❌ Error MongoDB: {e}", flush=True)