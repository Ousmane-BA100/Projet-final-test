# 🌦️ API d'Agrégation Météorologique

## 📋 Vue d'ensemble
API REST complète qui agrège des données météorologiques de plusieurs sources externes en appliquant les meilleures pratiques de développement (TDD, tests de charge, monitoring).

## 🎯 Objectifs pédagogiques
- Développement d'API REST avec une approche TDD
- Agrégation intelligente de sources multiples
- Tests complets (unitaires, intégration, contrat, charge)
- Monitoring et alertes en temps réel
- Gestion de la qualité et des performances

## 🚀 Fonctionnalités clés

### 1. Agrégation de données
- Récupération en temps réel depuis 3 sources :
  - OpenWeatherMap
  - WeatherAPI
  - OpenMeteo
- Calcul de moyennes pour :
  - Température
  - Humidité
  - Vitesse du vent
  - Direction du vent

### 2. Gestion du cache
- Mise en cache avec Redis
- Stratégie TTL (Time To Live) configurable
- Invalidation intelligente du cache

### 3. Monitoring
- Métriques temps réel avec Prometheus
- Tableaux de bord Grafana
- Surveillance des performances
- Alertes configurables

### 4. Tests complets
- Tests unitaires (pytest)
- Tests d'intégration
- Tests de charge (Locust)
- Tests de contrat

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



