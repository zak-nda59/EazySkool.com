# EazySkool - Base de Données

Ce document explique comment utiliser la base de données SQLite créée pour EazySkool.

## 📁 Structure des fichiers

- `database.sql` - Script SQL pour créer la base de données
- `database_manager.py` - Gestionnaire Python de la base de données
- `api_server.py` - Serveur API Flask pour connecter la DB au frontend
- `requirements.txt` - Dépendances Python
- `eazyskool.db` - Base de données SQLite (créée automatiquement)

## 🚀 Installation et démarrage

### 1. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

### 2. Créer la base de données

La base de données sera créée automatiquement lors du premier lancement :

```bash
python database_manager.py
```

### 3. Démarrer le serveur API

```bash
python api_server.py
```

Le serveur sera accessible sur : http://localhost:5000

## 🗄️ Structure de la base de données

### Tables principales

#### `users`
- Gestion des utilisateurs et authentification
- Champs : id, email, password_hash, first_name, last_name, city, created_at

#### `schools`
- Informations des écoles
- Champs : id, name, type_id, city_id, description, website, email, phone, address, latitude, longitude, average_rating, total_reviews

#### `school_types`
- Types d'écoles (Université, École de commerce, etc.)
- Champs : id, name, description

#### `cities`
- Villes du Grand Est
- Champs : id, name, region, latitude, longitude

#### `reviews`
- Avis des utilisateurs sur les écoles
- Champs : id, school_id, user_id, rating, comment, created_at

#### `favorites`
- Écoles favorites des utilisateurs
- Champs : id, user_id, school_id, created_at

#### `events`
- Événements (portes ouvertes, salons, etc.)
- Champs : id, title, description, event_date, event_time, location, school_id, is_online

#### `specializations`
- Spécialités/formations proposées
- Champs : id, name, description, category

### Tables de liaison

- `school_images` - Images des écoles
- `school_specializations` - Liaison écoles-spécialités

## 🔧 Utilisation de l'API

### Endpoints disponibles

#### Écoles
- `GET /api/schools` - Liste toutes les écoles
- `GET /api/schools/<id>` - Détails d'une école
- `GET /api/schools/search?q=query&city=ville&type=type` - Recherche d'écoles

#### Authentification
- `POST /api/auth/login` - Connexion utilisateur
- `POST /api/auth/register` - Création de compte

#### Favoris
- `GET /api/favorites` - Récupère les favoris d'un utilisateur
- `POST /api/favorites` - Ajoute un favori
- `DELETE /api/favorites` - Supprime un favori

#### Avis
- `POST /api/reviews` - Ajoute un avis

#### Données de référence
- `GET /api/cities` - Liste des villes
- `GET /api/types` - Types d'écoles
- `GET /api/events` - Événements à venir

### Exemples d'utilisation

#### Récupérer toutes les écoles
```bash
curl http://localhost:5000/api/schools
```

#### Rechercher des écoles
```bash
curl "http://localhost:5000/api/schools/search?q=Strasbourg&city=Strasbourg"
```

#### Créer un compte
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123","first_name":"John","last_name":"Doe"}'
```

## 💾 Données incluses

La base de données contient déjà :

### Écoles (8 écoles)
- Université de Strasbourg
- Université de Lorraine (Nancy)
- ICN Business School (Nancy)
- Sciences Po Strasbourg
- Université de Haute-Alsace (Mulhouse)
- INSA Strasbourg
- Université de Reims Champagne-Ardenne
- Université de Troyes

### Villes (6 villes)
- Strasbourg, Nancy, Mulhouse, Metz, Reims, Troyes

### Types d'écoles (6 types)
- Université, École de commerce, Institut d'études politiques, École d'ingénieur, École d'art, École de santé

### Spécialités (8 spécialités)
- Informatique, Médecine, Droit, Commerce, Ingénierie, Arts, Sciences, Langues

### Événements (4 événements)
- Portes ouvertes, Salon étudiant, Webinaire orientation, Journée découverte

## 🔄 Intégration avec le frontend

Pour connecter votre application JavaScript à la base de données, remplacez les données statiques par des appels API :

### Exemple de modification du script.js

```javascript
// Au lieu de ECOLES_GRAND_EST statique
async function loadSchools() {
    try {
        const response = await fetch('http://localhost:5000/api/schools');
        const data = await response.json();
        if (data.success) {
            return data.data;
        }
    } catch (error) {
        console.error('Erreur lors du chargement des écoles:', error);
    }
    return [];
}

// Utilisation
const schools = await loadSchools();
```

## 🛠️ Fonctionnalités avancées

### Export des données
```bash
curl http://localhost:5000/api/export
```

### Test de la base de données
```bash
python database_manager.py
```

## 📊 Vues SQL utiles

La base de données inclut des vues pré-créées :

- `schools_complete` - Écoles avec toutes les informations
- `reviews_with_users` - Avis avec informations utilisateur

## 🔒 Sécurité

- Les mots de passe sont hashés avec bcrypt
- Validation des données côté serveur
- Protection contre les injections SQL (utilisation de paramètres)

## 🚨 Dépannage

### Erreur "No module named 'bcrypt'"
```bash
pip install bcrypt
```

### Erreur "No module named 'flask'"
```bash
pip install flask flask-cors
```

### Base de données corrompue
Supprimez le fichier `eazyskool.db` et relancez :
```bash
python database_manager.py
```

## 📈 Évolutions futures

- Ajout de nouvelles écoles
- Système de notifications
- Statistiques avancées
- Système de modération des avis
- API pour applications mobiles 