import asyncio
from dotenv import load_dotenv
from src.services.weather_service import WeatherService

load_dotenv(override=True)

async def test_merged_weather():
    service = WeatherService()
    try:
        print("Test de la fusion des données météo...")
        data = await service.get_current_weather("Paris")
        print("\nRésultat fusionné :")
        print(f"Ville: {data.city}")
        print(f"Température: {data.temperature.current}°C")
        print(f"Ressenti: {data.temperature.feels_like}°C")
        print(f"Humidité: {data.humidity}%")
        print(f"Vent: {data.wind_speed} km/h, direction: {data.wind_direction}°")
        print(f"Description: {data.weather_description}")
        print(f"Source: {data.source}")
        print(f"Date: {data.timestamp}")
    except Exception as e:
        print(f"Erreur: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_merged_weather())