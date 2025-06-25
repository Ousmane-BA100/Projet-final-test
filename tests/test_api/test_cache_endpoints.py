from fastapi import status

def test_clear_cache(client):
    """Test de l'endpoint de nettoyage du cache"""
    # Test avec méthode POST
    response = client.post("/api/cache/clear")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success",
        "message": "Cache vidé avec succès"
    }
    
    # Test avec méthode non autorisée (GET)
    response = client.get("/api/cache/clear")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED