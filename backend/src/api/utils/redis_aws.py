import redis
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
redis_app = redis.from_url(os.getenv("REDIS_URL"))
