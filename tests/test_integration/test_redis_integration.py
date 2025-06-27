# tests/test_integration/test_redis_integration.py
import pytest
from httpx import AsyncClient
from src.main import app
from src.config.redis import get_redis

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_redis_integration(async_client):
    # Tester l'écriture dans Redis
    test_data = {"test": "value"}
    response = await async_client.post("/api/cache/test-key", json=test_data)
    assert response.status_code == 200
    assert response.json() == {"status": "success", "key": "test-key"}
    
    # Tester la lecture depuis Redis
    response = await async_client.get("/api/cache/test-key")
    assert response.status_code == 200
    assert response.json() == test_data

    # Tester la lecture d'une clé inexistante
    response = await async_client.get("/api/cache/non-existent-key")
    assert response.status_code == 404
    assert response.json()["detail"] == "Clé non trouvée dans le cache"

    # Nettoyer
    redis = await get_redis()
    await redis.delete("cache:test-key")