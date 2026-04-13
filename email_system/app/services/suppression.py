from app.core.redis_client import redis_client

PERM_KEY = "suppression:perm"
TEMP_KEY = "suppression:temp"

def add_block(email):
    redis_client.sadd(PERM_KEY, email)

def add_temp_block(email):
    redis_client.setex(f"temp:{email}", 3600, "1")  # 1 hour block

def is_blocked(email):
    if redis_client.sismember(PERM_KEY, email):
        return True

    if redis_client.exists(f"temp:{email}"):
        return True

    return False