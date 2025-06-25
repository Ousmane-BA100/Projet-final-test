import pytest
from unittest.mock import patch, AsyncMock
from src.services.weather_service import WeatherService, WeatherData
import time

@pytest.fixture
def mock_weather_data():
    return WeatherData(
        city="Paris",
        temperature={"current": 20.0, "feels_like": 18.0},
        humidity=60.0,
        wind_speed=10.0,
        wind_direction=180,
        weather_description="Cloudy",
        source="test",
        timestamp="2025-01-01T00:00:00"
    )

@pytest.mark.asyncio
async def test_get_cached_weather_hit(mock_weather_data):
    """Test du cache quand les données sont en cache"""
    service = WeatherService()
    # Utiliser un timestamp récent pour simuler un cache valide
    service._cache = {
        "paris": (mock_weather_data, time.time())  # timestamp actuel
    }
    service.cache_duration = 100  # Durée de cache valide

    with patch.object(service, 'get_current_weather', new_callable=AsyncMock) as mock_get:
        result = await service.get_cached_weather("Paris")
        mock_get.assert_not_called()  # Ne devrait pas appeler l'API
        assert result.city == "Paris"

@pytest.mark.asyncio
async def test_get_cached_weather_miss(mock_weather_data):
    """Test du cache quand les données ne sont pas en cache"""
    service = WeatherService()
    service._cache = {}
    service.cache_duration = 0  # Cache expiré
    
    with patch.object(service, 'get_current_weather', 
                     return_value=mock_weather_data) as mock_get:
        result = await service.get_cached_weather("Paris")
        mock_get.assert_called_once_with("Paris")
        assert result.city == "Paris"

@pytest.mark.asyncio
async def test_clear_cache():
    """Test de la suppression du cache"""
    service = WeatherService()
    service._cache = {"test": ("data", 0)}
    await service.clear_cache()
    assert len(service._cache) == 0