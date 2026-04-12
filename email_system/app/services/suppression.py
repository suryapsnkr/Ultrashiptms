# suppression.py
from app.core.redis_client import redis_client

SUPPRESSION_KEY = "suppression_set"

def is_blocked(email: str) -> bool:
    return redis_client.sismember(SUPPRESSION_KEY, email)

def add_block(email: str):
    redis_client.sadd(SUPPRESSION_KEY, email)