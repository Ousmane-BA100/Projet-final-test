import asyncio
from src.services.weather_service import WeatherService

async def test_openmeteo_service():
    service = WeatherService()
    try:
        print("Test OpenMeteo depuis le service...")
        data = await service._get_weather_from_openmeteo("Paris")
        if data:
            print(f"✓ Données reçues: {data.temperature.current}°C")
            print(f"Description: {data.weather_description}")
        else:
            print("✗ Aucune donnée reçue")
    except Exception as e:
        print(f"✗ Erreur: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_openmeteo_service())