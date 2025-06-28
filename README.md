# 🌦️ Projet : API Météo Agrégée avec Monitoring, Tests et CI/CD

## 1. 🎯 Vue d’ensemble

Ce projet est une API REST qui agrège des données météorologiques depuis plusieurs sources externes, les moyenne, les met en cache avec Redis, et expose les résultats via des endpoints. Le projet intègre un pipeline de tests automatisés, un monitoring Prometheus/Grafana, et un déploiement continu sur une instance EC2 via GitHub Actions.

---

## 2. 🔗 Sources de données & Agrégation

### Sources utilisées :
- **Open-Meteo** : Pas d’inscription, démarrage immédiat
- **OpenWeatherMap** : API clé gratuite
- **WeatherAPI** : Jusqu’à 1M de requêtes/mois

### Principe d’agrégation :
- Appels en parallèle aux APIs
- Traitement des erreurs (fallback si une API tombe)
- Agrégation par moyenne :
  - Moyenne de température et humidité
  - Fusion de descriptions météo (choix de la source la plus prioritaire)

### Exemple de réponse API :
```json
{
  "city": "Paris",
  "timestamp": "2025-06-28T14:00:00Z",
  "temperature": {
    "current": 21.3,
    "unit": "celsius"
  },
  "humidity": 68,
  "description": "Partly cloudy",
  "sources": ["openweather", "weatherapi"]
}
```


### 2. ⚡ Gestion du cache avancée

#### Architecture
- **Moteur de cache** : Redis en tant que solution de stockage clé-valeur haute performance
- **Format des clés** : `weather:{ville_en_minuscules}` (ex: `weather:paris`)
- **Durée de vie** : 10 minutes par défaut (configurable via `CACHE_DURATION`)

#### Fonctionnalités clés
- **Mise en cache automatique** : Toutes les requêtes météo sont automatiquement mises en cache
- **Incrustation intelligente** : Le cache est mis à jour de manière asynchrone lors des lectures
- **Gestion des erreurs** : Le système continue de fonctionner même si Redis est indisponible
- **Sérialisation JSON** : Les données sont stockées en format JSON pour une meilleure interopérabilité

#### Avantages
- ⚡ **Réduction de la latence** : Jusqu'à 10x plus rapide pour les données en cache
- 💰 **Économie de coûts** : Moins d'appels aux APIs externes
- 📈 **Meilleure disponibilité** : Fonctionne même en cas de panne des fournisseurs
- 🔄 **Fraisage progressif** : Les anciennes données restent disponibles pendant le rafraîchissement

#### Configuration
```python
# Dans .env
REDIS_HOST=redis       # Hôte Redis
REDIS_PORT=6379       # Port Redis
```

### 3. 🧪 Stratégie de test complète

#### Tests Unitaires
- **Objectif** : Vérifier le bon fonctionnement des composants individuels
- **Framework** : Pytest avec pytest-asyncio
- **Couverture** : 
  - Logique métier des services
  - Transformation des données
  - Gestion des erreurs
- **Exemple** : [tests/test_services/test_weather_service.py](cci:7://file:///c:/Users/bousm/Downloads/Projet-Final-Test/tests/test_services/test_weather_service.py:0:0-0:0)
- **Résultats** : [Voir le log des tests](tests/test_services/test_output.log)

#### Tests d'Intégration
- **Objectif** : Vérifier les interactions entre les composants
- **Points clés** :
  - Intégration avec Redis
  - Communication entre services
  - Gestion des dépendances externes
- **Exemple** : [tests/test_integration/test_redis_integration.py](cci:7://file:///c:/Users/bousm/Downloads/Projet-Final-Test/tests/test_integration/test_redis_integration.py:0:0-0:0)
- **Résultats** : [Voir le log des tests](tests/test_integration/test_output.log)

#### Tests de Contrat
- **Objectif** : Assurer la cohérence des réponses API
- **Vérifications** :
  - Structure des réponses
  - Types de données
  - Champs obligatoires
- **Exemple** : [tests/test_contract/test_weather_contract.py](cci:7://file:///c:/Users/bousm/Downloads/Projet-Final-Test/tests/test_contract/test_weather_contract.py:0:0-0:0)
- **Résultats** : [Voir le log des tests](tests/test_contract/test_output.log)

#### Tests d'API
- **Couverture** :
  - Points de terminaison REST
  - Codes d'état HTTP
  - Gestion des erreurs
  - Validation des entrées
- **Exemple** : [tests/test_api/test_weather_endpoints.py](cci:7://file:///c:/Users/bousm/Downloads/Projet-Final-Test/tests/test_api/test_weather_endpoints.py:0:0-0:0)
- **Résultats** : [Voir le log des tests](tests/test_api/test_output.log)

#### Tests de Performance (Load Testing)
- **Outil** : Locust
- **Scénarios** :
  - Simulation de 100 utilisateurs simultanés
  - Tests de montée en charge progressive
  - Mesure des temps de réponse
- **Métriques** :
  - Requêtes par seconde
  - Temps de réponse moyen
  - Taux d'échec
- **Exemple** : [tests/test_load/test_weather_load_test.py](cci:7://file:///c:/Users/bousm/Downloads/Projet-Final-Test/tests/test_load/test_weather_load_test.py:0:0-0:0)
- **Résultats** : [Voir le log des tests](tests/test_load/test_output.log)

#### Exemple d'exécution des Tests

```bash
# Exécuter les tests dans un conteneur Docker
docker-compose exec app bash -c "pytest -v tests/test_load/ --asyncio-mode=auto" | tee tests/test_load/test_output.log
```


###  Monitoring
- Métriques temps réel avec Prometheus
- Tableaux de bord Grafana
- Surveillance des performances
- Alertes configurables

## 🛠️ Installation

### Prérequis
- Python 3.9+
- Redis
- Docker (optionnel)

### Configuration
1. Copier le fichier [.env-exemple](cci:7://file:///c:/Users/bousm/Downloads/Projet-Final-Test/.env-exemple:0:0-0:0) vers `.env`
2. Remplir les variables d'environnement :
   ```env
   OPENWEATHER_API_KEY=votre_cle
   WEATHERAPI_KEY=votre_cle
   REDIS_HOST=localhost
   REDIS_PORT=6379

### 🐳 Avec Docker
```bash
docker-compose up -d
```

## 📊 Monitoring
Accédez aux outils de monitoring :

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

## 🧪 Exécution des tests
```bash
# Tests unitaires
pytest tests/unit/

# Tests d'intégration
pytest tests/integration/

# Tests de charge
locust -f tests/load/locustfile.py
```
## 🔄 Déploiement
Le déploiement est automatisé via GitHub Actions vers AWS EC2 :
1. Exécution des tests
2. Construction de l'image Docker
3. Déploiement sur l'instance EC2

## 📚 Documentation API
- Documentation interactive : http://localhost:8000/docs
- Documentation ReDoc : http://localhost:8000/redoc

## 📈 Métriques surveillées
- Temps de réponse des API
- Taux d'utilisation du cache
- Taux d'erreur
- Utilisation des ressources



