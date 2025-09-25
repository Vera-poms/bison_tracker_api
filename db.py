from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()

#Connect to Mongo Atlas Cluster
mongo_client = MongoClient(os.getenv("MONGO_URI"))


# Access database
bison_guard_db = mongo_client["bison_guard_db"]


# Pick a connection to operate on
bisons_collection = bison_guard_db["bisons"]
statistics = bison_guard_db["streaming_stats"]