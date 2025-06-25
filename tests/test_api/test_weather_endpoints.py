def test_get_weather(client):
    response = client.get("/weather/Paris")
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Paris"
    assert "temperature" in data

def test_get_weather_invalid_city(client):
    """Test avec une ville invalide"""
    response = client.get("/weather/InvalidCity123")
    assert response.status_code == 500
    # Vérifier que la réponse contient un message d'erreur
    error_data = response.json()
    assert "detail" in error_data
    assert "Impossible de récupérer" in error_data["detail"]