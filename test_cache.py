import asyncio
import time
from src.services.weather_service import WeatherService

async def test_cache():
    service = WeatherService()
    
    # Premier appel - devrait faire un appel API
    print("\nPremier appel (doit faire un appel API) :")
    data1 = await service.get_cached_weather("Paris")
    print(f"Température: {data1.temperature.current}°C")
    
    # Deuxième appel - devrait utiliser le cache
    print("\nDeuxième appel (doit utiliser le cache) :")
    data2 = await service.get_cached_weather("Paris")
    print(f"Température: {data2.temperature.current}°C")
    
    # Vider le cache
    print("\nVidage du cache...")
    service.cache_duration = 0  # Pour forcer l'expiration
    
    # Troisième appel - devrait refaire un appel API
    print("\nTroisième appel (doit refaire un appel API) :")
    data3 = await service.get_cached_weather("Paris")
    print(f"Température: {data3.temperature.current}°C")

if __name__ == "__main__":
    asyncio.run(test_cache())