import asyncio
import httpx

async def test_openmeteo():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 48.8566,  # Paris
        "longitude": 2.3522,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m,weather_code",
        "timezone": "auto"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            print("Réponse OpenMeteo reçue !")
            print(f"Température actuelle: {data['current']['temperature_2m']}°C")
    except Exception as e:
        print(f"Erreur OpenMeteo: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_openmeteo())