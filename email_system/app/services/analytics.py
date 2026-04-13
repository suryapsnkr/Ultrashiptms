from app.core.redis_client import redis_client

def track_event(event_type):
    redis_client.incr(f"stats:{event_type}")

def get_stats():
    return {
        "sent": int(redis_client.get("stats:sent") or 0),
        "failed": int(redis_client.get("stats:failed") or 0),
        "bounced": int(redis_client.get("stats:bounced") or 0),
    }