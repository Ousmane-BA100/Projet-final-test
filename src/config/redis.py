import os
from redis.asyncio import Redis
from typing import Optional

redis_client = None

async def init_redis():
    global redis_client
    try:
        # Forcer la valeur de l'hôte à "redis" pour Docker Compose
        host = "redis"  # Forcer la valeur
        port = int(os.getenv("REDIS_PORT", 6379))
        
        print(f"🔌 Tentative de connexion à Redis sur {host}:{port}")  # Debug
        
        redis_client = Redis(
            host=host,
            port=port,
            db=int(os.getenv("REDIS_DB", 0)),
            socket_connect_timeout=5,
            socket_keepalive=True,
            decode_responses=True
        )
        await redis_client.ping()
        print("✅ Connecté à Redis avec succès")
        return redis_client
    except Exception as e:
        print(f"❌ Erreur de connexion à Redis: {e}")
        print(f"REDIS_HOST: {os.getenv('REDIS_HOST')}")  # Debug
        print(f"REDIS_PORT: {os.getenv('REDIS_PORT')}")  # Debug
        raise

async def get_redis() -> Redis:
    if redis_client is None:
        await init_redis()
    return redis_client