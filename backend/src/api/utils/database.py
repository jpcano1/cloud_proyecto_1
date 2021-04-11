from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient

load_dotenv(find_dotenv())

db = MongoClient(os.getenv("MONGO_URI"))[os.getenv("MONGO_DB")]